webpackJsonp([8],{RFMV:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=s("woOf"),n=s.n(a),r={name:"SellItem",props:{modal_type:"",singleItem:{username:"",password:"",page_level:"",comment:"",item_number:""}},data:function(){return{ruleValidate:{username:[{required:!0,message:"请输入名称"}],password:[{required:!0,message:"请输入密码"}],page_level:[{required:!0,message:"请输入级别"},{type:"number",message:"错误金额"}],comment:[{required:!1,message:"请输入备注",trigger:"blur"},{type:"string",max:200,message:"太长不易读",trigger:"blur"}]}}},methods:{handleSubmit:function(e){var t=this;this.$refs[e].validate(function(e){if(e){if("modify"==t.$props.modal_type){var s="/setting/user/"+t.singleItem.item_number;t.$http.put(s,t.singleItem).then(function(e){var s=e.data;"success"!=s.status&&t.$Message.error(s.message),t.$Message.success("修改成功!"),t.$emit("closeModal","submit")},function(e){401==e.status&&t.$router.push({name:"login"})})}else if("add"==t.$props.modal_type){s="/setting/user/1";t.$http.post(s,t.singleItem).then(function(e){var s=e.data;"success"!=s.status&&t.$Message.error(s.message),t.$Message.success("新增成功!"),t.$emit("closeModal","submit")},function(e){401==e.status&&t.$router.push({name:"login"})})}}else t.$Message.error("请查看是否填写完必须输入的项!")})},handleReset:function(e){this.$refs[e].resetFields()}}},i={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("Row",[s("Form",{ref:"singleItem",attrs:{model:e.singleItem,rules:e.ruleValidate,"label-width":80}},[s("FormItem",{staticStyle:{display:"none"},attrs:{label:"单号",prop:"item"}},[s("Input",{attrs:{disabled:""},model:{value:e.singleItem.item_number,callback:function(t){e.$set(e.singleItem,"item_number",t)},expression:"singleItem.item_number"}})],1),e._v(" "),s("FormItem",{attrs:{label:"登陆用户",prop:"username"}},[s("Input",{attrs:{placeholder:"请输入登陆用户名称（譬如手机号）"},model:{value:e.singleItem.username,callback:function(t){e.$set(e.singleItem,"username",t)},expression:"singleItem.username"}})],1),e._v(" "),s("FormItem",{attrs:{label:"登陆密码",prop:"password"}},[s("Input",{attrs:{type:"password",placeholder:"请输入登陆密码"},model:{value:e.singleItem.password,callback:function(t){e.$set(e.singleItem,"password",t)},expression:"singleItem.password"}})],1),e._v(" "),s("FormItem",{attrs:{label:"权限级别",prop:"page_level"}},[s("InputNumber",{attrs:{max:5,min:1,placeholder:"请输入权限级别"},model:{value:e.singleItem.page_level,callback:function(t){e.$set(e.singleItem,"page_level",t)},expression:"singleItem.page_level"}})],1),e._v(" "),s("FormItem",{attrs:{label:"备注",prop:"comment"}},[s("Input",{attrs:{type:"textarea",autosize:{minRows:2,maxRows:5},placeholder:"可以输入备注以便记录"},model:{value:e.singleItem.comment,callback:function(t){e.$set(e.singleItem,"comment",t)},expression:"singleItem.comment"}})],1),e._v(" "),s("FormItem",[s("Button",{attrs:{type:"primary"},on:{click:function(t){e.handleSubmit("singleItem")}}},[e._v("提交")]),e._v(" "),s("Button",{staticStyle:{"margin-left":"8px"},on:{click:function(t){e.handleReset("singleItem")}}},[e._v("重置")])],1)],1)],1)},staticRenderFns:[]},o={name:"UserManage",components:{User:s("VU/8")(r,i,!1,null,null,null).exports},data:function(){var e=this;return{singleItem:{},modal_type:"modify",modal_title:"",singleModal:!1,search:"",page:1,page_size:20,total_count:0,order:"desc",order_key:"created_time",users_data:[],columns:[{title:"编号",key:"raw_id",width:80},{title:"登陆用户用户名",key:"username",sortable:"custom"},{title:"权限级别",key:"page_level",sortable:"custom"},{title:"备注",key:"comment",ellipsis:!0,sortable:"custom"},{title:"更新时间",key:"created_time",sortable:"custom"},{title:"Action",key:"action",width:150,align:"center",render:function(t,s){return t("div",[t("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){e.modifyItem(s.index)}}},"编辑"),t("Button",{props:{type:"error",size:"small"},on:{click:function(){e.removeItem(s.index)}}},"删除")])}}]}},computed:{},watch:{},created:function(){this.getUsers()},methods:{getUsers:function(){var e=this,t="/setting/users?";t+="page="+this.page,t+="&page_size="+this.page_size,t+="&order="+this.order,t+="&order_key="+this.order_key,this.$http.post(t,{search:this.search}).then(function(t){var s=t.data;e.users_data=s.data,e.total_count=s.total_count,e.page=s.page,"success"!=s.status&&e.$Message.error(s.message)},function(t){403==t.status?e.$Message.error("权限不足，请申请权限"):401==t.status&&e.$router.push({name:"login"})})},handleSearch:function(e){this.search=e,this.getUsers()},modifyItem:function(e){this.singleModal=!0,this.modal_type="modify",this.modal_title="修改登陆用户",this.singleItem=n()({},this.users_data[e])},changePage:function(e){this.page=e,this.getUsers()},changePageSize:function(e){this.page_size=e,this.getUsers()},sortChange:function(e){this.order=e.order,this.order_key=e.key,this.getUsers()},visibleChange:function(e){this.singleModal=e},closeModal:function(e){this.singleModal=!1,this.getUsers()},removeItem:function(e){var t=this;this.$Modal.confirm({title:"是否确认删除",content:"",onOk:function(){var s="/setting/user/"+t.users_data[e].item_number;t.$http.delete(s).then(function(e){var s=e.data;"success"!=s.status&&t.$Message.error(s.message),t.$Message.success("删除成功!"),t.getUsers()},function(e){403==e.status?t.$Message.error("权限不足，请申请权限"):401==e.status&&t.$router.push({name:"login"})})},onCancel:function(){}})},addItem:function(){this.modal_type="add",this.modal_title="增加登陆用户",this.singleItem={},this.singleModal=!0}}},l={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"4"}},[s("Button",{attrs:{type:"primary",shape:"circle"},on:{click:e.addItem}},[e._v("添加")])],1),e._v(" "),s("Col",{attrs:{span:"8",offset:"12"}},[s("Input",{staticStyle:{width:"300px",float:"right"},attrs:{search:"","enter-button":"",placeholder:"请输入关键字搜索"},on:{"on-search":e.handleSearch},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"start"}},[s("Col",{attrs:{span:"24"}},[s("Table",{attrs:{border:"",columns:e.columns,data:e.users_data},on:{"on-sort-change":e.sortChange}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"24"}},[s("Page",{staticStyle:{float:"right"},attrs:{total:e.total_count,"show-total":"","show-sizer":"",current:e.page,"page-size":e.page_size,"page-size-opts":[20,50,100,500]},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)],1),e._v(" "),s("Modal",{attrs:{"footer-hide":"",title:e.modal_title},on:{"on-visible-change":e.visibleChange},model:{value:e.singleModal,callback:function(t){e.singleModal=t},expression:"singleModal"}},[s("User",{attrs:{singleItem:e.singleItem,modal_type:e.modal_type},on:{closeModal:e.closeModal}})],1)],1)},staticRenderFns:[]},c=s("VU/8")(o,l,!1,null,null,null).exports;t.default=c}});
//# sourceMappingURL=8.05de958f6dc5f3739112.js.map