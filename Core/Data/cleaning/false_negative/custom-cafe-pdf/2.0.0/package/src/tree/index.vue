<template>
  <ul>
    <li v-for="(item, index) of list" :key="item.title + index" class="item">
      <div class="item-title" @click="itemClick(item)">
        <i
          v-if="item.items.length > 0"
          @click.stop="toggle(item)"
          class="icon"
          :class="[{ 'up-arrow': item.show }]"
        ></i>
        <em>{{ item.title }}</em>
      </div>
      <transition name="fade">
        <div
          v-if="item.items.length > 0"
          v-show="item.show"
          class="item-children"
          :key="item.title"
        >
          <tree-list v-on="$listeners" v-bind="$attrs" :list="item.items" />
        </div>
      </transition>
    </li>
  </ul>
</template>
<script>
export default {
  name: 'TreeList',
  props: {
    list: {
      type: Array,
    },
  },
  mixins: [],
  components: {},
  data() {
    return {
      select: null,
    };
  },
  computed: {},
  watch: {},
  methods: {
    itemClick(item) {
      this.$emit('item-click', item);
    },
    toggle(item) {
      item.show = !item.show;
    },
  },
};
</script>
<style>
.pdf-catalogue {
  width: 200px;
  height: 100%;
  padding: 0 5px;
  overflow: auto;
  font-size: 14px;
  background-color: rgb(0 0 0 / 10%);
}
.pdf-catalogue ul {
  list-style: none;
}
.pdf-catalogue .item-children {
  padding-left: 15px;
}
.pdf-catalogue .item-title {
  margin: 5px 0;
  cursor: pointer;
}
.pdf-catalogue .item-title.active {
  color: rgb(0 0 0 / 90%);
  background-color: rgb(0 0 0 / 15%);
}
.pdf-catalogue .item-title em {
  display: block;
  margin-left: 15px;
  font-style: normal;
  line-height: 1;
}
.pdf-catalogue .icon {
  position: relative;
  top: 2px;
  float: left;
  width: 0;
  height: 0;
  cursor: pointer;
  border-top: 5px solid transparent;
  border-right: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 5px solid #555;
}
.pdf-catalogue .up-arrow {
  top: 5px;
  border-top: 5px solid #555;
  border-right: 5px solid transparent;
  border-bottom: 5px solid transparent;
  border-left: 5px solid transparent;
}
.fade-enter,
.fade-leave-to {
  height: 0;
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  height: auto;
  transition: all 0.3s;
}
</style>
