webpackJsonp([11],{Qa7A:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a={name:"SalaryRecord",data:function(){return{search:"",page:1,page_size:20,total_count:0,order:"desc",order_key:"created_time",items_data:[],columns:[{title:"编号",key:"raw_id",width:80},{title:"员工手机号",key:"phone_number",sortable:"custom"},{title:"姓名",key:"name",sortable:"custom"},{title:"提成比例",key:"percentage",sortable:"custom"},{title:"客户消费金额",key:"sell_item_money",sortable:"custom"},{title:"个人所得金额",key:"money",sortable:"custom"},{title:"单号",key:"sell_item_number",sortable:"custom"},{title:"入账原因",key:"reason",sortable:"custom"},{title:"记录时间",key:"created_time",sortable:"custom"}]}},computed:{},watch:{},created:function(){this.getItems()},methods:{getItems:function(){var e=this,t="/employee_money_history?";t+="page="+this.page,t+="&page_size="+this.page_size,t+="&order="+this.order,t+="&order_key="+this.order_key,this.$http.post(t,{search:this.search}).then(function(t){var s=t.data;e.items_data=s.data,e.total_count=s.total_count,e.page=s.page,"success"!=s.status&&e.$Message.error(s.message)},function(t){401==t.status&&e.$router.push({name:"login"})})},handleSearch:function(e){this.search=e,this.getItems()},changePage:function(e){this.page=e,this.getItems()},changePageSize:function(e){this.page_size=e,this.getItems()},sortChange:function(e){this.order=e.order,this.order_key=e.key,this.getItems()}}},o={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[s("Row",{staticClass:"code-row-bg",attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"8"}},[s("Input",{staticStyle:{width:"300px",float:"right"},attrs:{search:"","enter-button":"",placeholder:"请输入关键字搜索"},on:{"on-search":e.handleSearch},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"start"}},[s("Col",{attrs:{span:"24"}},[s("Table",{attrs:{border:"",columns:e.columns,data:e.items_data},on:{"on-sort-change":e.sortChange}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"24"}},[s("Page",{staticStyle:{float:"right"},attrs:{total:e.total_count,"show-total":"","show-sizer":"",current:e.page,"page-size":e.page_size,"page-size-opts":[20,50,100,500]},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)],1)],1)},staticRenderFns:[]},r=s("VU/8")(a,o,!1,null,null,null).exports;t.default=r}});
//# sourceMappingURL=11.bbda77d5020248f70c27.js.map