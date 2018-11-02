webpackJsonp([12],{vzVe:function(e,t,s){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var a=s("woOf"),l=s.n(a),i={name:"SellItem",props:{modal_type:"",employee_type_list:"",singleItem:{name:"",phone_number:"",first_day:"",employee_type:"",base_salary:0,percentage:0,status:"",item_number:""}},data:function(){return{ruleValidate:{name:[{required:!0,message:"请输入名称",trigger:"blur"}],phone_number:[{required:!0,message:"请输入电话号码"},{type:"number",message:"错误格式"}],first_day:[{required:!0,message:"请选择日期"}],employee_type:[{required:!0,message:"请选择员工类型"}],base_salary:[{required:!0,message:"请填写底薪"},{type:"number",message:"错误格式"}],percentage:[{required:!0,message:"请填写提成比率"},{type:"float",message:"错误提成比率格式"}],status:[{required:!0,message:"请选择状态",trigger:"blur"}]}}},methods:{handleSubmit:function(e){var t=this;this.$refs[e].validate(function(s){if(s){if("modify"==t.$props.modal_type){var a="/employee/"+t.singleItem.phone_number;(i=l()({},t.singleItem)).first_day=i.first_day.toString(),t.$http.put(a,i).then(function(s){var a=s.data;"success"!=a.status?t.$Message.error(a.message):(t.$Message.success("修改成功!"),t.$emit("closeModal","submit"),t.$refs[e].resetFields())},function(e){401==e.status&&t.$router.push({name:"login"})})}else if("add"==t.$props.modal_type){var i;a="/employee/1";(i=l()({},t.singleItem)).first_day=i.first_day.toString(),t.$http.post(a,i).then(function(s){var a=s.data;"success"!=a.status?t.$Message.error(a.message):(t.$Message.success("新增成功!"),t.$emit("closeModal","submit"),t.$refs[e].resetFields())},function(e){401==e.status&&t.$router.push({name:"login"})})}}else t.$Message.error("请查看是否填写完必须输入的项!")})},handleReset:function(e){this.$refs[e].resetFields()}}},n={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("Row",[s("Form",{ref:"singleItem",attrs:{model:e.singleItem,rules:e.ruleValidate,"label-width":80}},[s("FormItem",{staticStyle:{display:"none"},attrs:{label:"单号",prop:"item"}},[s("Input",{attrs:{disabled:""},model:{value:e.singleItem.item_number,callback:function(t){e.$set(e.singleItem,"item_number",t)},expression:"singleItem.item_number"}})],1),e._v(" "),s("FormItem",{attrs:{label:"姓名",prop:"name"}},[s("Input",{attrs:{placeholder:"请输入姓名"},model:{value:e.singleItem.name,callback:function(t){e.$set(e.singleItem,"name",t)},expression:"singleItem.name"}})],1),e._v(" "),s("FormItem",{attrs:{label:"手机号",prop:"phone_number"}},["add"!=e.modal_type?s("InputNumber",{staticStyle:{width:"280px"},attrs:{disabled:"",placeholder:"请输入手机号"},model:{value:e.singleItem.phone_number,callback:function(t){e.$set(e.singleItem,"phone_number",t)},expression:"singleItem.phone_number"}}):e._e(),e._v(" "),"add"==e.modal_type?s("InputNumber",{staticStyle:{width:"280px"},attrs:{placeholder:"请输入手机号"},model:{value:e.singleItem.phone_number,callback:function(t){e.$set(e.singleItem,"phone_number",t)},expression:"singleItem.phone_number"}}):e._e()],1),e._v(" "),s("FormItem",{attrs:{label:"入职日期",prop:"first_day"}},[s("DatePicker",{staticStyle:{width:"200px"},attrs:{type:"date",placeholder:"Select date"},model:{value:e.singleItem.first_day,callback:function(t){e.$set(e.singleItem,"first_day",t)},expression:"singleItem.first_day"}})],1),e._v(" "),s("FormItem",{attrs:{label:"员工类型",prop:"employee_type"}},[s("Select",{attrs:{placeholder:"请选择员工类别"},model:{value:e.singleItem.employee_type,callback:function(t){e.$set(e.singleItem,"employee_type",t)},expression:"singleItem.employee_type"}},e._l(e.employee_type_list,function(t,a){return s("Option",{key:a,attrs:{value:t.value}},[e._v(e._s(t.label))])}))],1),e._v(" "),s("FormItem",{attrs:{label:"底薪",prop:"base_salary"}},[s("InputNumber",{staticStyle:{width:"180px"},attrs:{min:0,placeholder:"请输入提成比率"},model:{value:e.singleItem.base_salary,callback:function(t){e.$set(e.singleItem,"base_salary",t)},expression:"singleItem.base_salary"}})],1),e._v(" "),s("FormItem",{attrs:{label:"提成比率",prop:"percentage"}},[s("InputNumber",{staticStyle:{width:"180px"},attrs:{max:1,min:0,step:.1,placeholder:"请输入提成比率"},model:{value:e.singleItem.percentage,callback:function(t){e.$set(e.singleItem,"percentage",t)},expression:"singleItem.percentage"}})],1),e._v(" "),s("FormItem",{attrs:{label:"状态",prop:"status"}},[s("RadioGroup",{model:{value:e.singleItem.status,callback:function(t){e.$set(e.singleItem,"status",t)},expression:"singleItem.status"}},[s("Radio",{attrs:{label:"在职"}},[e._v("在职")]),e._v(" "),s("Radio",{attrs:{label:"离职"}},[e._v("离职")])],1)],1),e._v(" "),s("FormItem",[s("Button",{attrs:{type:"primary"},on:{click:function(t){e.handleSubmit("singleItem")}}},[e._v("提交")]),e._v(" "),s("Button",{staticStyle:{"margin-left":"8px"},on:{click:function(t){e.handleReset("singleItem")}}},[e._v("重置")])],1)],1)],1)},staticRenderFns:[]},o={name:"EmployeeList",components:{EmployeeItem:s("VU/8")(i,n,!1,null,null,null).exports},data:function(){var e=this;return{employee_type_list:[],singleItem:{},modal_type:"modify",modal_title:"",singleModal:!1,search:"",page:1,page_size:20,total_count:0,order:"desc",order_key:"created_time",employee_list_data:[],columns:[{title:"编号",key:"raw_id",width:80},{title:"姓名",key:"name",sortable:"custom"},{title:"手机号",key:"phone_number",sortable:"custom"},{title:"入职日期",key:"first_day",sortable:"custom",render:function(e,t){if(""!=t.row.first_day)return e("div",new Date(t.row.first_day).toLocaleDateString())}},{title:"员工类型",key:"employee_type",sortable:"custom"},{title:"底薪",key:"base_salary",sortable:"custom"},{title:"提成比率",key:"percentage",sortable:"custom"},{title:"状态",key:"status",sortable:"custom"},{title:"更新时间",key:"created_time",sortable:"custom"},{title:"Action",key:"action",width:150,align:"center",render:function(t,s){return t("div",[t("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){e.modifyItem(s.index)}}},"编辑"),t("Button",{props:{type:"error",size:"small"},on:{click:function(){e.removeItem(s.index)}}},"删除")])}}]}},computed:{},watch:{},created:function(){this.getEmployeeLists(),this.getEmployeeTypeList()},methods:{getEmployeeLists:function(){var e=this,t="/employees?";t+="page="+this.page,t+="&page_size="+this.page_size,t+="&order="+this.order,t+="&order_key="+this.order_key,this.$http.post(t,{search:this.search}).then(function(t){var s=t.data;e.employee_list_data=s.data,e.total_count=s.total_count,e.page=s.page,"success"!=s.status&&e.$Message.error(s.message)},function(t){401==t.status&&e.$router.push({name:"login"})})},getEmployeeTypeList:function(){var e=this;this.$http.get("/summarized_setting").then(function(t){var s=t.data;e.employee_type_list=s.employee_type_list,"success"!=s.status&&e.$Message.error(s.message)},function(t){401==t.status&&e.$router.push({name:"login"})})},handleSearch:function(e){this.search=e,this.getEmployeeLists()},modifyItem:function(e){this.singleModal=!0,this.modal_type="modify",this.modal_title="修改员工信息",this.singleItem=l()({},this.employee_list_data[e]),""!=this.singleItem.first_day&&(this.singleItem.first_day=new Date(this.singleItem.first_day))},changePage:function(e){this.page=e,this.getEmployeeLists()},changePageSize:function(e){this.page_size=e,this.getEmployeeLists()},sortChange:function(e){this.order=e.order,this.order_key=e.key,this.getEmployeeLists()},visibleChange:function(e){this.singleModal=e},closeModal:function(e){this.singleModal=!1,this.getEmployeeLists()},removeItem:function(e){var t=this;this.$Modal.confirm({title:"是否确认删除",content:"",onOk:function(){var s="/employee/"+t.employee_list_data[e].phone_number;t.$http.delete(s).then(function(e){var s=e.data;"success"!=s.status?t.$Message.error(s.message):(t.$Message.success("删除成功!"),t.getEmployeeLists())},function(e){401==e.status&&t.$router.push({name:"login"})})},onCancel:function(){}})},addItem:function(){this.modal_type="add",this.modal_title="新增员工",this.singleItem={},this.singleItem.first_day="",this.singleModal=!0}}},r={render:function(){var e=this,t=e.$createElement,s=e._self._c||t;return s("div",[s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"4"}},[s("Button",{attrs:{type:"primary",shape:"circle"},on:{click:e.addItem}},[e._v("添加")])],1),e._v(" "),s("Col",{attrs:{span:"8",offset:"12"}},[s("Input",{staticStyle:{width:"300px",float:"right"},attrs:{search:"","enter-button":"",placeholder:"请输入关键字搜索"},on:{"on-search":e.handleSearch},model:{value:e.search,callback:function(t){e.search=t},expression:"search"}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"start"}},[s("Col",{attrs:{span:"24"}},[s("Table",{attrs:{border:"",columns:e.columns,data:e.employee_list_data},on:{"on-sort-change":e.sortChange}})],1)],1),e._v(" "),s("Row",{staticClass:"code-row-bg",staticStyle:{padding:"10px"},attrs:{type:"flex",justify:"end"}},[s("Col",{attrs:{span:"24"}},[s("Page",{staticStyle:{float:"right"},attrs:{total:e.total_count,"show-total":"","show-sizer":"",current:e.page,"page-size":e.page_size,"page-size-opts":[20,50,100,500]},on:{"on-change":e.changePage,"on-page-size-change":e.changePageSize}})],1)],1),e._v(" "),s("Modal",{attrs:{"footer-hide":"",title:e.modal_title},on:{"on-visible-change":e.visibleChange},model:{value:e.singleModal,callback:function(t){e.singleModal=t},expression:"singleModal"}},[s("EmployeeItem",{attrs:{singleItem:e.singleItem,modal_type:e.modal_type,employee_type_list:e.employee_type_list},on:{closeModal:e.closeModal}})],1)],1)},staticRenderFns:[]},m=s("VU/8")(o,r,!1,null,null,null).exports;t.default=m}});
//# sourceMappingURL=12.12c180117227d95ec4c5.js.map