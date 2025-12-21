import cafePdf from './index.vue';
cafePdf.install = function (Vue) {
  Vue.component(cafePdf.name, cafePdf);
};
if (typeof window !== 'undefined' && window.Vue) {
  window.cafePdf = cafePdf;
  window.Vue.use(cafePdf);
}
export default cafePdf;
