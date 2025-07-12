import os
import datetime
from packj.util.enum_util import PackageManagerEnum, LanguageEnum

def log_install_command(cmd, pm_enum, pkg_name, ver_str, log_file="/home/ubuntu/packj/packj/audit/install_commands.log"):
    """
    Log the install command to a file
    
    Args:
        cmd: Generated command
        pm_enum: Package manager enum
        pkg_name: Package name
        ver_str: Version string
        log_file: Log file path
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file) if os.path.dirname(log_file) else '.', exist_ok=True)
    
    log_entry = f"[{timestamp}] PM: {pm_enum} | Package: {pkg_name} | Version: {ver_str or 'latest'} | Command: {cmd}\n"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def get_pm_install_cmd(pm_enum, pkg_name, ver_str, quiet=True, log_file=None):
    """
    Original function with minimal log enhancement
    """
    # 打印传入的参数
    print(f"DEBUG - get_pm_install_cmd parameters:")
    print(f"  pm_enum: {pm_enum} (type: {type(pm_enum)})")
    print(f"  pkg_name: {pkg_name} (type: {type(pkg_name)})")
    print(f"  ver_str: {ver_str} (type: {type(ver_str)})")
    print(f"  quiet: {quiet} (type: {type(quiet)})")
    print(f"  log_file: {log_file} (type: {type(log_file)})")
    
    if pm_enum == PackageManagerEnum.pypi:
        base_cmd = 'pip3 install '
        quiet_args = '--quiet --no-warn-script-location --disable-pip-version-check '
        ver_cmd = f'=={ver_str}'
    elif pm_enum == PackageManagerEnum.npmjs:
        base_cmd = f'npm install'
        quiet_args = ' --silent --no-progress --no-update-notifier '
        ver_cmd = f'@{ver_str}'
    elif pm_enum == PackageManagerEnum.rubygems:
        base_cmd = 'gem install --user'
        quiet_args = ' --silent '
        ver_cmd = f' -v {ver_str}'
    elif pm_enum == PackageManagerEnum.local_nodejs:
        # 对于local_nodejs，检查是否存在对应的tarball文件
        base_cmd = f'npm install'
        quiet_args = ' --silent --no-progress --no-update-notifier '
        ver_cmd = ''
        
    else:
        raise Exception(f'Package manager {pm_enum} is not supported')

    cmd = base_cmd
    if quiet:
        cmd += quiet_args
    cmd += f' {pkg_name}'
    if ver_str and pm_enum != PackageManagerEnum.local_nodejs:
        cmd += ver_cmd
    
    # Log the command if log_file is provided
    if log_file:
        log_install_command(cmd, pm_enum, pkg_name, ver_str, log_file)
    # 打印最终生成的命令
    print(f"DEBUG - Final command: {cmd}")
    return cmd

def get_pm_enum(pm_name):
	if pm_name == 'pypi':
		return PackageManagerEnum.pypi
	elif pm_name == 'npm':
		return PackageManagerEnum.npmjs
	elif pm_name == 'rubygems':
		return PackageManagerEnum.rubygems
	elif pm_name == 'local_nodejs':
		return PackageManagerEnum.local_nodejs
	elif pm_name == 'local_python':
		return PackageManagerEnum.local_python
	elif pm_name == 'cargo':
		return PackageManagerEnum.rust
	elif pm_name == 'packagist':
		return PackageManagerEnum.php
	elif pm_name == 'maven':
		return PackageManagerEnum.maven
	elif pm_name == 'nuget':
		return PackageManagerEnum.nuget
	else:
		raise Exception(f'Package manager {pm_name} is not supported')

def get_pm_proxy_for_language(language, registry=None, cache_dir=None, isolate_pkg_info=False):
	from packj.util.enum_util import LanguageEnum
	if language == LanguageEnum.python:
		from packj.audit.pm_proxy.pypi import PypiProxy
		return PypiProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif language == LanguageEnum.javascript:
		from packj.audit.pm_proxy.npmjs import NpmjsProxy
		return NpmjsProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif language == LanguageEnum.ruby:
		from packj.audit.pm_proxy.rubygems import RubygemsProxy
		return RubygemsProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	else:
		raise Exception("PM proxy not available for language: %s" % language)

def get_pm_proxy(pm, registry=None, cache_dir=None, isolate_pkg_info=False):
	from packj.util.enum_util import PackageManagerEnum
	if pm == PackageManagerEnum.pypi:
		from packj.audit.pm_proxy.pypi import PypiProxy
		return PypiProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.local_python:
		from packj.audit.pm_proxy.local_python import LocalPythonProxy
		return LocalPythonProxy(cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.npmjs:
		from packj.audit.pm_proxy.npmjs import NpmjsProxy
		return NpmjsProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.rubygems:
		from packj.audit.pm_proxy.rubygems import RubygemsProxy
		return RubygemsProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.local_nodejs:
		from packj.audit.pm_proxy.local_nodejs import LocalNodeJSProxy
		return LocalNodeJSProxy(cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.rust:
		from packj.audit.pm_proxy.rust import RustProxy
		return RustProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.php:
		from packj.audit.pm_proxy.packagist_php import PackagistProxy
		return PackagistProxy(registry=registry, cache_dir=cache_dir, isolated_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.maven:
		from packj.audit.pm_proxy.maven import MavenProxy
		return MavenProxy(registry=registry, cache_dir=cache_dir, isolated_pkg_info=isolate_pkg_info)
	elif pm == PackageManagerEnum.nuget:
		from packj.audit.pm_proxy.nuget import NugetProxy
		return NugetProxy(registry=registry, cache_dir=cache_dir, isolate_pkg_info=isolate_pkg_info)
	else:
		raise Exception("PM proxy not available for package manager: %s" % pm)
