#!/usr/bin/env python3

import feedparser
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from configs.config import MonitorConfig
from database import get_db_manager, PyGuardTaskLogger
from crawler.utils import download_pkg, depresspkg
from crawler.cascade_tools import CascadeToos


NPM_PACKAGES_DIR = Path("/home2/wenbo/Documents/NPMAnalysis/Dataset/npm")
NPM_UPDATE_DIR = NPM_PACKAGES_DIR / "updatepkgs"
NPM_UNZIP_DIR = NPM_PACKAGES_DIR / "unzip"


class NPMCollector:
    def __init__(self, rss_url: str = "https://registry.npmjs.org/-/rss", data_dir: Optional[str] = None,
                 task_logger: Optional[PyGuardTaskLogger] = None):
        self.rss_url = rss_url
        self.registry_url = "https://registry.npmjs.org"
        self.extension_tgz = ".tgz"

        if data_dir is None:
            MonitorConfig.ensure_monitor_dirs()
            self.download_dir = MonitorConfig.NPM_UPDATE_DIR
            self.unzip_dir = MonitorConfig.NPM_UNZIP_DIR
        else:
            self.data_dir = Path(data_dir)
            self.download_dir = self.data_dir / "updatepkgs"
            self.unzip_dir = self.data_dir / "unzip"

        self.sascadetoos = CascadeToos()
        self.processed_packages = set()
        self.task_logger = task_logger
        self.current_task_id = None


    def fetch_data(self):
        try:
            feed = feedparser.parse(self.rss_url)
            if feed.bozo == 0:
                return feed
            print("[NPM] Failed to parse RSS feed")
            return None
        except Exception as e:
            print(f"[NPM] Error fetching RSS: {e}")
            return None


    def detectpkg(self, fullpath: str, pkgname: str, version: str, package_metadata: Optional[Dict] = None):
        unzip_path = depresspkg(fullpath, pkgname, version, str(self.unzip_dir))
        self.sascadetoos.detect_main("update", pkgname, version, fullpath, unzip_path, package_metadata)


    def get_package_info(self, package_name: str) -> Optional[Dict]:
        try:
            encoded_name = requests.utils.quote(package_name, safe='/')
            response = requests.get(f"{self.registry_url}/{encoded_name}", timeout=15)
            if response.status_code == 200:
                return response.json()
            print(f"[NPM] Failed to fetch registry data for {package_name}: HTTP {response.status_code}")
            return None
        except Exception as e:
            print(f"[NPM] Error getting info for {package_name}: {e}")
            return None


    def _select_tarball(self, package_name: str, package_info: Dict) -> Optional[Dict]:
        dist_tags = package_info.get("dist-tags", {})
        versions = package_info.get("versions", {})
        latest_version = dist_tags.get("latest")

        if not latest_version or latest_version not in versions:
            return None

        version_data = versions.get(latest_version, {})
        tarball_url = version_data.get("dist", {}).get("tarball")
        if not tarball_url:
            return None

        filename = tarball_url.split("/")[-1] or self._build_filename(package_name, latest_version)

        return {
            "version": latest_version,
            "filename": filename,
            "url": tarball_url,
            "author": (version_data.get("author") or {}).get("name") or package_info.get("author", ""),
            "description": version_data.get("description") or package_info.get("description", "")
        }


    def _build_filename(self, package_name: str, version: str) -> str:
        safe_name = package_name.replace("/", "-").replace("@", "")
        return f"{safe_name}-{version}{self.extension_tgz}"


    def parse_data(self, feed):
        try:
            db = get_db_manager()
            items = feed.entries if feed else []

            if self.task_logger:
                self.current_task_id = self.task_logger.create_task(
                    task_type="scheduled",
                    trigger_source="cron"
                )
                self.task_logger.update_total_packages(self.current_task_id, len(items))

            for item in items:
                package_name = (item.get("title") or "").strip()
                if not package_name:
                    continue

                if package_name in self.processed_packages:
                    continue

                description = item.get("description", "")
                author = item.get("author", "") or item.get("dc_creator", "")
                publish_time = item.get("published", "") or item.get("updated", "")

                print(f"[NPM] Processing package: {package_name}")

                package_info = self.get_package_info(package_name)
                if not package_info:
                    continue

                tarball_info = self._select_tarball(package_name, package_info)
                if not tarball_info:
                    print(f"[NPM] No downloadable versions discovered for {package_name}")
                    if self.task_logger and self.current_task_id:
                        self.task_logger.add_package_result(
                            self.current_task_id,
                            package_name=package_name,
                            version="unknown",
                            status="failed",
                            error="No downloadable versions discovered"
                        )
                        self.task_logger.add_error(
                            self.current_task_id,
                            error_type="download",
                            message="No downloadable versions discovered",
                            package_name=package_name
                        )
                    continue

                version = tarball_info["version"]
                process_key = f"{package_name}@{version}"
                if process_key in self.processed_packages:
                    continue

                download_link = tarball_info["url"]
                selected_filename = tarball_info["filename"]

                try:
                    existing_record = db.get_package_record(package_name, version, "npm")
                    if existing_record:
                        print(f"[NPM] Package {package_name} {version} already analyzed, skipping...")
                        if self.task_logger and self.current_task_id:
                            self.task_logger.add_package_result(
                                self.current_task_id,
                                package_name=package_name,
                                version=version,
                                status="skipped",
                                download_link=download_link,
                                error="Already analyzed in database"
                            )
                        self.processed_packages.add(process_key)
                        continue

                    pkg_start_time = datetime.now()
                    download_time = pkg_start_time.isoformat()

                    save_path = download_pkg(
                        str(self.download_dir),
                        package_name,
                        version,
                        selected_filename,
                        download_link
                    )
                    print(f"[NPM] Downloaded to: {save_path}")

                    package_metadata = {
                        "download_link": download_link,
                        "author": author or tarball_info.get("author", ""),
                        "description": description or tarball_info.get("description", ""),
                        "publish_time": publish_time,
                        "download_time": download_time,
                        "package_manager": "npm",
                        "registry_link": item.get("link")
                    }

                    self.detectpkg(save_path, package_name, version, package_metadata)
                    print(f"[NPM] Detection completed: {package_name}@{version}")

                    pkg_end_time = datetime.now()
                    pkg_duration = (pkg_end_time - pkg_start_time).total_seconds()

                    if self.task_logger and self.current_task_id:
                        detection_record = db.get_package_record(package_name, version, "npm")
                        detection_results = detection_record.get("detection_results", {}) if detection_record else {}

                        self.task_logger.add_package_result(
                            self.current_task_id,
                            package_name=package_name,
                            version=version,
                            status="success",
                            download_link=download_link,
                            detection_results=detection_results,
                            start_time=pkg_start_time,
                            end_time=pkg_end_time,
                            duration=pkg_duration
                        )

                    self.processed_packages.add(process_key)

                except Exception as e:
                    print(f"[NPM] Error processing {package_name}@{version}: {e}")
                    if self.task_logger and self.current_task_id:
                        self.task_logger.add_package_result(
                            self.current_task_id,
                            package_name=package_name,
                            version=version,
                            status="failed",
                            download_link=download_link,
                            error=str(e)
                        )
                        self.task_logger.add_error(
                            self.current_task_id,
                            error_type="detection",
                            message=str(e),
                            package_name=package_name
                        )

            if self.task_logger and self.current_task_id:
                self.task_logger.complete_task(self.current_task_id, status="completed")

        except Exception as e:
            print(f"[NPM] Error in parse_data: {e}")
            if self.task_logger and self.current_task_id:
                self.task_logger.fail_task(self.current_task_id, f"Error in parse_data: {str(e)}")


if __name__ == '__main__':
    while True:
        collector = NPMCollector()
        data = collector.fetch_data()
        if data:
            collector.parse_data(data)
