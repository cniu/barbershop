webpackJsonp([14],{HPLP:function(t,a,e){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var s=e("lp6y"),r=e("U4e1"),n={name:"Dashboard",components:{ChartPie:s.b,ChartBar:s.a,InforCard:r.a},data:function(){return{inforCardData:[{title:"开单总数",icon:"md-locate",count:0,color:"#19be6b"},{title:"营业额（仅开单）",icon:"md-share",count:0,color:"#ed3f14"},{title:"均价（仅开单）",icon:"md-chatbubbles",count:0,color:"#ff9900"}],sell_item_type:[],assistant_sell_number:[],hairdresser_sell_number:[],employee_analysis_result:[],info:"如下信息为当月的数据分析"}},created:function(){},mounted:function(){var t=this;this.$nextTick(function(){t.getDailyData("now")})},methods:{getDailyData:function(t){var a=this,e="/get_employee_data/"+t;this.$http.get(e).then(function(t){var e=t.data;a.inforCardData[0].count=e.data.items_count,a.inforCardData[1].count=e.data.sell_number,a.inforCardData[2].count=0,0!=e.data.items_count&&(a.inforCardData[2].count=(e.data.sell_number/e.data.items_count).toFixed(2)),a.sell_item_type=e.data.sell_item_type,a.hairdresser_sell_number=e.data.hairdresser_sell_number,a.assistant_sell_number=e.data.assistant_sell_number,a.employee_analysis_result=e.data.employee_analysis_result,"success"!=e.status&&a.$Message.error(e.message)},function(t){401==t.status&&a.$router.push({name:"login"})})},updateInfo:function(t){""===t?(t="now",this.info="如下为当月的数据分析"):this.info="如下为 "+t+" 的数据分析",this.getDailyData(t)}}},i={render:function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",[e("Row",[e("Col",{attrs:{span:"4"}},[e("div",[e("span",[t._v(t._s(t.info))])])]),t._v(" "),e("Col",{attrs:{span:"16"}},[e("DatePicker",{staticStyle:{width:"200px",height:"40px","padding-bottom":"10px",float:"right"},attrs:{type:"year",placeholder:"请选择年份"},on:{"on-change":t.updateInfo}})],1),t._v(" "),e("Col",{attrs:{span:"4"}},[e("DatePicker",{staticStyle:{width:"200px",height:"40px","padding-bottom":"10px",float:"right"},attrs:{type:"month",placeholder:"请选择月份"},on:{"on-change":t.updateInfo}})],1)],1),t._v(" "),e("Row",{attrs:{gutter:20}},t._l(t.inforCardData,function(a,s){return e("i-col",{key:"infor-"+s,staticStyle:{height:"120px","padding-bottom":"10px"},attrs:{xs:12,md:8,lg:4}},[e("infor-card",{attrs:{shadow:"",color:a.color,icon:a.icon,"icon-size":36}},[e("div",[e("span",{staticStyle:{"font-size":"35px"}},[t._v(t._s(a.count))])]),t._v(" "),e("p",[t._v(t._s(a.title))])])],1)})),t._v(" "),e("Row",{staticStyle:{"margin-top":"10px"},attrs:{gutter:20}},[e("i-col",{staticStyle:{"margin-bottom":"20px"},attrs:{md:24,lg:8}},[e("Card",{attrs:{shadow:""}},[e("chart-pie",{staticStyle:{height:"300px"},attrs:{value:t.sell_item_type,text:"客户开单服务类别"}})],1)],1),t._v(" "),e("i-col",{staticStyle:{"margin-bottom":"20px"},attrs:{md:24,lg:8}},[e("Card",{attrs:{shadow:""}},[e("chart-pie",{staticStyle:{height:"300px"},attrs:{value:t.hairdresser_sell_number,text:"发型师营业额"}})],1)],1),t._v(" "),e("i-col",{staticStyle:{"margin-bottom":"20px"},attrs:{md:24,lg:8}},[e("Card",{attrs:{shadow:""}},[e("chart-pie",{staticStyle:{height:"300px"},attrs:{value:t.assistant_sell_number,text:"助理营业额"}})],1)],1)],1),t._v(" "),e("Row",{attrs:{gutter:20}},t._l(t.employee_analysis_result,function(t,a){return e("i-col",{key:"info-"+a,staticStyle:{"margin-bottom":"20px"},attrs:{md:24,lg:8}},[e("Card",{attrs:{shadow:""}},[e("chart-pie",{staticStyle:{height:"300px"},attrs:{value:t.content,text:t.name}})],1)],1)}))],1)},staticRenderFns:[]},o=e("VU/8")(n,i,!1,null,null,null).exports;a.default=o}});
//# sourceMappingURL=14.a9996829baa319384a5e.js.map