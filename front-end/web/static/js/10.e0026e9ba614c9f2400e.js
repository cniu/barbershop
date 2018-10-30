webpackJsonp([10],{"Ilp+":function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var l=s("woOf"),a=s.n(l),i={name:"SellItem",props:{hairdresser_list:"",assistant_list:"",fellow_list:"",modal_type:"",singleItem:{hairdresser:"",assistant:"",item_type:[],money:"",pay_type:"",fellow:"",comment:"",item_number:""}},data:function(){return{ruleValidate:{hairdresser:[{required:!0,message:"请选择发型师"}],assistant:[{required:!0,message:"请选择助理"}],pay_type:[{required:!0,message:"请选择付款类型"}],money:[{required:!0,message:"请填写金额"},{type:"number",message:"错误金额"}],item_type:[{required:!0,type:"array",message:"请选择消费类型"}],fellow:[{required:!1,message:"请输入会员手机号"}],comment:[{required:!1,message:"请输入备注",trigger:"blur"},{type:"string",max:200,message:"太长不易读",trigger:"blur"}]}}},methods:{handleSubmit:function(e){var t=this;this.$refs[e].validate(function(e){if(e){if("modify"==t.$props.modal_type){var s="/sell_item/"+t.singleItem.item_number;t.$http.put(s,t.singleItem).then(function(e){var s=e.data;"success"!=s.status&&t.$Message.error(s.message),t.$Message.success("修改成功!"),t.$emit("closeModal","submit")},function(e){401==e.status&&t.$router.push({name:"login"})})}else if("add"==t.$props.modal_type){s="/sell_item/1";t.singleItem.item_type=t.singleItem.item_type.join(","),t.$http.post(s,t.singleItem).then(function(e){var s=e.data;"success"!=s.status&&t.$Message.error(s.message),t.$Message.success("新增成功!"),t.$emit("closeModal","submit")},function(e){401==e.status&&t.$router.push({name:"login"})})}}else t.$Message.error("请查看是否填写完必须输入的项!")})},handleReset:function(e){this.$refs[e].resetFields()},showFellowInfo:function(){var e=this,t=this.fellow_list.filter(function(t){return t.value==e.singleItem.fellow}),s="<p>姓名："+t[0].name+"</p><p>卡类型："+t[0].card_type+"</p><p>余额："+t[0].money+"</p><p>手机号："+t[0].value+"</p>";this.$Modal.success({title:"会员信息",content:s})},getFellowList:function(e){}}},n={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("Row",[s("Form",{ref:"singleItem",attrs:{model:e.singleItem,rules:e.ruleValidate,"label-width":80}},[s("FormItem",{staticStyle:{display:"none"},attrs:{label:"单号",prop:"item"}},[s("Input",{attrs:{disabled:""},model:{value:e.singleItem.item_number,callback:function(t){e.$set(e.singleItem,"item_number",t)},expression:"singleItem.item_number"}})],1),e._v(" "),s("FormItem",{attrs:{label:"发型师",prop:"hairdresser"}},[s("Select",{attrs:{placeholder:"请选择发型师"},model:{value:e.singleItem.hairdresser,callback:function(t){e.$set(e.singleItem,"hairdresser",t)},expression:"singleItem.hairdresser"}},e._l(e.hairdresser_list,function(t,l){return s("Option",{key:l,attrs:{value:t.value}},[e._v(e._s(t.label))])}))],1),e._v(" "),s("FormItem",{attrs:{label:"助理",prop:"assistant"}},[s("Select",{attrs:{placeholder:"请选择助理"},model:{value:e.singleItem.assistant,callback:function(t){e.$set(e.singleItem,"assistant",t)},expression:"singleItem.assistant"}},e._l(e.assistant_list,function(t,l){return s("Option",{key:l,attrs:{value:t.value}},[e._v(e._s(t.label))])}))],1),e._v(" "),s("FormItem",{attrs:{label:"消费类型",prop:"item_type"}},[s("CheckboxGroup",{model:{value:e.singleItem.item_type,callback:function(t){e.$set(e.singleItem,"item_type",t)},expression:"singleItem.item_type"}},[s("Checkbox",{attrs:{label:"染发"}}),e._v(" "),s("Checkbox",{attrs:{label:"烫发"}}),e._v(" "),s("Checkbox",{attrs:{label:"假发"}}),e._v(" "),s("Checkbox",{attrs:{label:"洗头"}})],1)],1),e._v(" "),s("FormItem",{attrs:{label:"消费金额",prop:"money"}},[s("InputNumber",{staticStyle:{width:"180px"},attrs:{placeholder:"请输入金额"},model:{value:e.singleItem.money,callback:function(t){e.$set(e.singleItem,"money",t)},expression:"singleItem.money"}})],1),e._v(" "),s("FormItem",{attrs:{label:"付款类型",prop:"pay_type"}},[s("RadioGroup",{model:{value:e.singleItem.pay_type,callback:function(t){e.$set(e.singleItem,"pay_type",t)},expression:"singleItem.pay_type"}},[s("Radio",{attrs:{label:"现金"}},[e._v("现金")]),e._v(" "),s("Radio",{attrs:{label:"微信"}},[e._v("微信")]),e._v(" "),s("Radio",{attrs:{label:"支付宝"}},[e._v("支付宝")]),e._v(" "),s("Radio",{attrs:{label:"刷卡"}},[e._v("刷卡")])],1)],1),e._v(" "),s("FormItem",{attrs:{label:"会员",prop:"fellow"}},[s("Row",[s("Col",{attrs:{span:"16"}},[s("Select",{staticStyle:{width:"180px"},attrs:{filterable:""},model:{value:e.singleItem.fellow,callback:function(t){e.$set(e.singleItem,"fellow",t)},expression:"singleItem.fellow"}},e._l(e.fellow_list,function(t,l){return s("Option",{key:l,attrs:{value:t.value}},[e._v(e._s(t.label))])}))],1),e._v(" "),s("Col",{attrs:{span:"8"}},[s("Button",{attrs:{type:"primary",size:"small"},on:{click:e.showFellowInfo}},[e._v("查看会员信息")])],1)],1)],1),e._v(" "),s("FormItem",{attrs:{label:"备注",prop:"comment"}},[s("Input",{attrs:{type:"textarea",autosize:{minRows:2,maxRows:5},placeholder:"可以输入备注以便记录"},model:{value:e.singleItem.comment,callback:function(t){e.$set(e.singleItem,"comment",t)},expression:"singleItem.comment"}})],1),e._v(" "),s("FormItem",[s("Button",{attrs:{type:"primary"},on:{click:function(t){e.handleSubmit("singleItem")}}},[e._v("Submit")]),e._v(" "),s("Button",{staticStyle:{"margin-left":"8px"},on:{click:function(t){e.handleReset("singleItem")}}},[e._v("Reset")])],1)],1)],1)},staticRenderFns:[]},o={name:"SellItems",components:{SellItem:s("VU/8")(i,n,!1,null,null,null).exports},data:function(){var e=this;return{singleItem:{},modal_type:"modify",singleModal:!1,search:"",page:1,page_size:20,total_count:0,order:"desc",order_key:"created_time",sell_items_data:[],assistant_list:[],hairdresser_list:[],fellow_list:[],columns:[{title:"编号",key:"raw_id",width:80},{title:"单号",key:"item_number",sortable:"custom"},{title:"发型师",key:"hairdresser",sortable:"custom"},{title:"助理",key:"assistant",sortable:"custom"},{title:"消费类型",key:"item_type",sortable:"custom"},{title:"金额",key:"money",sortable:"custom"},{title:"付款类型",key:"pay_type",sortable:"custom"},{title:"会员",key:"fellow",sortable:"custom"},{title:"备注",key:"comment",sortable:"custom"},{title:"开单时间",key:"created_time",sortable:"custom"},{title:"Action",key:"action",width:150,align:"center",render:function(t,s){return t("div",[t("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){e.modifyItem(s.index)}}},"编辑")])}}]}},computed:{},watch:{},created:function(){this.getSellItems(),this.getEmployees(),this.getFellows()},methods:{getSellItems:function(){var e=this,t="/sell_items?";t+="page="+this.page,t+="&page_size="+this.page_size,t+="&order="+this.order,t+="&order_key="+this.order_key,this.$http.post(t,{search:this.search}).then(function(t){var s=t.data;e.sell_items_data=s.data,e.total_count=s.total_count,e.page=s.page,"success"!=s.status&&e.$Message.error(s.message)},function(t){401==t.status&&e.$router.push({name:"login"})})},getEmployees:function(){var e=this;this.$http.get("/summarized_employees").then(function(t){var s=t.data;e.hairdresser_list=s.hairdresser_list,e.assistant_list=s.assistant_list,"success"!=s.status&&e.$Message.error(s.message)},function(t){401==t.status&&e.$router.push({name:"login"})})},getFellows:function(){var e=this;this.$http.get("/summarized_fellows").then(function(t){var s=t.data;e.fellow_list=s.response_list,"success"!=s.status&&e.$Message.error(s.message)},function(t){401==t.status&&e.$router.push({name:"login"})})},handleSearch:function(e){this.search=e,this.getSellItems()},show:function(e){this.$Modal.info({title:"User Info",content:"Name："+this.sell_items_data[e].name+"<br>Age："+this.sell_items_data[e].age+"<br>Address："+this.sell_items_data[e].address})},modifyItem:function(e){this.singleModal=!0,this.singleItem=a()({},this.sell_items_data[e]),this.singleItem.item_type=this.singleItem.item_type.split(",")},remove:function(e){this.sell_items_data.splice(e,1)},changePage:function(e){this.page=e,this.getSellItems()},changePageSize:function(e){this.page_size=e,this.getSellItems()},sortChange:function(e){this.order=e.order,this.order_key=e.key,this.getSellItems()},visibleChange:function(e){this.singleModal=e},closeModal:function(e){this.singleModal=!1,this.getSellItems()}}},r={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[s("Row",{staticClass:"code-row-bg",attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"8"}},[s("Input",{staticStyle:{width:"300px",float:"right"},attrs:{search:"","enter-button":"",placeholder:"请输入关键字搜索"},on:{"on-search":e.handleSearch},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"start"}},[s("Col",{attrs:{span:"24"}},[s("Table",{attrs:{border:"",columns:e.columns,data:e.sell_items_data},on:{"on-sort-change":e.sortChange}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"24"}},[s("Page",{staticStyle:{float:"right"},attrs:{total:e.total_count,"show-total":"","show-sizer":"",current:e.page,"page-size":e.page_size,"page-size-opts":[20,50,100,500]},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)],1),e._v(" "),s("Modal",{attrs:{"footer-hide":"",title:"修改单子"},on:{"on-visible-change":e.visibleChange},model:{value:e.singleModal,callback:function(t){e.singleModal=t},expression:"singleModal"}},[s("SellItem",{attrs:{singleItem:e.singleItem,modal_type:e.modal_type,hairdresser_list:e.hairdresser_list,assistant_list:e.assistant_list,fellow_list:e.fellow_list},on:{closeModal:e.closeModal}})],1)],1)},staticRenderFns:[]},m=s("VU/8")(o,r,!1,null,null,null).exports;t.default=m}});
//# sourceMappingURL=10.e0026e9ba614c9f2400e.js.map