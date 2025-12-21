<template>
  <div class="pdf-box" :style="style">
    <div v-if="$slots.header" class="pdf-header">
      <slot name="header"></slot>
    </div>
    <div class="pdf-body">
      <div
        v-if="catalogue && catalogue.length > 0 && showNav"
        class="pdf-catalogue"
      >
        <tree :list="catalogue" @item-click="nav" />
      </div>
      <div class="pdf-container" ref="container" @scroll="fnScroll">
        <div class="pdf-viewer" ref="viewer"></div>
      </div>
    </div>
    <div v-if="$slots.footer" class="pdf-footer">
      <slot name="footer"></slot>
    </div>
    <div v-if="pageLoading" class="page-loading">
      <em>{{ loadingNum }} / {{ countNum }}</em>
      <progress
        class="page-progress"
        :value="loadingNum"
        :max="countNum"
      ></progress>
    </div>
  </div>
</template>
<script>
import Tree from './tree/index.vue';
import PDFLib from './plugin/pdfjs-dist/webpack';
import {
  PDFLinkService,
  PDFViewer,
  EventBus,
} from './plugin/pdfjs-dist/web/pdf_viewer.js';
import './plugin/pdfjs-dist/web/pdf_viewer.css';
import CMapReaderFactory from './plugin/CMapReaderFactory.js';
export default {
  name: 'cafePdf',
  props: {
    filePath: {
      type: String,
      required: true,
    },
    width: {
      type: String,
      default: '100%',
    },
    height: {
      type: String,
      default: '100%',
    },
    showNav: {
      type: Boolean,
      default: true,
    },
    useOnlyCssZoom: {
      type: Boolean,
      default: false,
    },
    autoWidth: {
      type: Boolean,
      default: false,
    },
    textLayerMode: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      countPage: null,
      currentPage: 1,
      pageLoading: false,
      loadingNum: 0,
      countNum: 100,
      timer: null,
      pdfViewer: null,
      pdfLoadingTask: null,
      linkService: null,
      catalogue: null,
      scale: 'auto',
      fnScroll: () => {},
    };
  },
  components: {
    Tree,
  },
  computed: {
    style() {
      const { width, height } = this;
      const fixedWidth = /(%|px)/.test(width) ? width : `${width}px`;
      const fixedHeight = /(%|px)/.test(height) ? height : `${height}px`;
      return {
        width: fixedWidth,
        height: fixedHeight,
      };
    },
  },
  watch: {
    filePath: {
      handler(newVal) {
        if (newVal) {
          this.initViewer();
        }
      },
    },
  },
  created() {
    this.fnScroll = this.fnThrottle(this.handleScroll, 200);
  },
  mounted() {
    this.initViewer();
  },
  beforeDestroy() {
    this.destroyView();
  },
  methods: {
    traversalData(data) {
      for (let i = 0; i < data.length; i++) {
        data[i].show = false;
        if (data[i].items.length > 0) {
          this.traversalData(data[i].items);
        }
      }
      return data;
    },
    nav(item) {
      this.linkService.navigateTo(item.dest);
    },
    initViewer() {
      const that = this;
      const eventBus = new EventBus();
      this.loading();
      this.linkService = new PDFLinkService();
      this.pdfViewer = new PDFViewer({
        container: this.$refs.container,
        useOnlyCssZoom: this.useOnlyCssZoom,
        textLayerMode: this.textLayerMode,
        linkService: this.linkService,
        eventBus: eventBus,
      });
      this.linkService.setViewer(this.pdfViewer);
      this.pdfViewer.currentScaleValue = this.scale;
      eventBus.on('pagesinit', () => {
        that.pdfViewer.currentScaleValue = that.scale;
      });
      this.pdfLoadingTask = PDFLib.getDocument({
        url: this.filePath,
        CMapReaderFactory,
      });
      this.pdfLoadingTask.promise
        .then((pdfDoc) => {
          this.catalogue = null;
          this.pdfViewer.setDocument(pdfDoc);
          this.linkService.setDocument(pdfDoc);
          if (this.showNav) {
            pdfDoc.getOutline().then((outline) => {
              if (outline) {
                this.catalogue = this.traversalData(outline);
              }
            });
          }
          this.countPage = pdfDoc.numPages;
          this.$emit('on-success', this.countPage, pdfDoc);
          this.pdfViewer._currentScale = 1;
          this.loadingNum = 100;
          clearInterval(this.timer);
          this.pageLoading = false;
        })
        .catch((error) => {
          clearInterval(this.timer);
          this.pageLoading = false;
          this.$emit('on-error', error);
        });
    },
    fnThrottle(fn, delay, atleast) {
      let timer = null;
      let previous = null;
      return function () {
        const now = +new Date();
        if (!previous) {
          previous = now;
        }
        if (atleast && now - previous > atleast) {
          fn();
          previous = now;
          clearTimeout(timer);
        } else {
          clearTimeout(timer);
          timer = setTimeout(() => {
            fn();
            previous = null;
          }, delay);
        }
      };
    },
    handleScroll() {
      const scrolled = this.$refs.container.scrollTop;
      this.currentPage = this.pdfViewer._currentPageNumber;
      this.$emit('on-scroll', this.currentPage, this.pdfViewer, scrolled);
    },
    prePage() {
      this.goToPage(--this.currentPage);
    },
    nextPage() {
      this.goToPage(++this.currentPage);
    },
    changeScale(scale) {
      this.scale = scale;
      this.pdfViewer.currentScaleValue = this.scale;
    },
    goToPage(page) {
      if (page < 1 || page > this.countPage) {
        return;
      }
      this.pdfViewer.currentPageNumber = page;
    },
    loading() {
      this.pageLoading = true;
      this.loadingNum = 0;
      this.countNum = 100;
      this.timer = setInterval(() => {
        this.loadingNum += Math.floor(Math.random() * 3 + 1);
        if (this.loadingNum > 95) {
          clearInterval(this.timer);
        }
      }, 40);
    },
    async getPDF(scale) {
      this.pageLoading = true;
      this.loadingNum = 0;
      this.countNum = this.countPage;
      const print = document.querySelector('#print-container');
      if (!print) {
        const container = document.createElement('div');
        container.setAttribute('id', 'print-container');
        document.body.appendChild(container);
      } else {
        print.innerHTML = '';
      }
      const pdf = await PDFLib.getDocument(this.filePath);
      for (let i = 1; i <= pdf.numPages; i++) {
        try {
          // eslint-disable-next-line no-await-in-loop
          await this.rendPDF(pdf, i, scale);
          this.loadingNum = i;
        } catch (e) {
          this.pageLoading = false;
        }
      }
      this.pageLoading = false;
      window.print();
    },
    async rendPDF(pdf, num, scale) {
      const page = await pdf.getPage(num);
      const container = document.querySelector('#print-container');
      const viewport = page.getViewport(scale);
      const pageDiv = document.createElement('div');
      pageDiv.setAttribute('id', `page-${page.pageIndex + 1}`);
      container.appendChild(pageDiv);
      const canvas = document.createElement('canvas');
      pageDiv.appendChild(canvas);
      const context = canvas.getContext('2d');
      canvas.height = viewport.height;
      canvas.width = viewport.width;
      const renderContext = {
        canvasContext: context,
        viewport: viewport,
      };
      await page.render(renderContext);
    },
    printFile(scale = 1.5) {
      this.getPDF(scale);
    },
    rotatePages(delta) {
      this.pdfViewer.pagesRotation += delta;
    },
    rotateCW() {
      this.rotatePages(90);
    },
    rotateCCW() {
      this.rotatePages(-90);
    },
    destroyView() {
      this.pdfLoadingTask.destroy();
      this.pdfViewer = null;
      this.linkService = null;
      this.pdfLoadingTask = null;
      this.timer = null;
    },
  },
};
</script>
<style>
.pdf-box {
  position: relative;
  display: flex;
  overflow: hidden;
  flex-direction: column;
}
.pdf-header {
  padding: 5px;
  background-color: rgb(249 249 250);
  border-bottom: 1px solid #d2d2d2;
}
.pdf-body {
  position: relative;
  display: flex;
  overflow: hidden;
  flex: 1;
}
.pdf-container {
  position: relative;
  overflow: auto;
  flex: 1;
}
.pdf-body .page,
.pdf-body .textLayer {
  margin: 0 auto;
}
.pdf-body .page {
  position: relative;
}
.pdf-footer {
  padding: 5px;
  background-color: rgb(249 249 250);
  border-top: 1px solid #d2d2d2;
}
#print-container {
  display: none;
}
.page-loading {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 9999;
  width: 100%;
  height: 100%;
  text-align: center;
  background-color: rgb(0 0 0 / 50%);
}
.page-loading em {
  display: block;
  margin-top: 10%;
  font-style: normal;
  color: #fff;
}
@media print {
  .pdf-box {
    display: none;
  }
  #print-container {
    display: block;
  }
}
</style>
