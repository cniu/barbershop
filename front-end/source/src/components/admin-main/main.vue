<style lang="less" scoped>
@import 'main.less';
</style>
<template>
  <section class="admin-layout-container">
      <div class="layout">
        <Layout>
            <Sider ref="side1" hide-trigger collapsible :collapsed-width="78" v-model="isCollapsed" style="background: rgb(73, 80, 96);">
                <div class="logo" >
                    <img :src="logo" width="100" v-if="!isCollapsed"/>
                    <Avatar icon="ios-book" size="large" v-else/>
                </div>
                <Menu 
                    ref="side_menu"
                    :active-name="activeMenuName" 
                    :open-names="openMenuName"
                    theme="dark"
                    width="auto" 
                    :class="menuitemClasses"
                    @on-select="choosedMenu"
                    v-if="!isCollapsed">
                    <template v-for="(menu,menu_index) in menus">
                        <Submenu :name="menu.name" v-if="menu.children">
                            <template slot="title">
                                <Icon :size="20" :type="menu.icon"></Icon>
                                {{menu.title}}
                            </template>
                            <MenuItem :name="child.name" v-for="(child ,child_index) in menu.children" :key="child_index">
                                <Icon :size="20" :type="child.icon"></Icon>
                                {{child.title}}
                            </MenuItem>
                        </Submenu>
                        <MenuItem :name="menu.name" v-if="!menu.children && menu.showInMenus">
                             <Icon :size="20" :type="menu.icon"></Icon>
                            {{menu.title}}
                        </MenuItem>
                    </template>                    
                </Menu>
                <div class="dropdown-wrap">
                    <template v-for="(menu,menu_index) in menus" v-if="isCollapsed">
                        <Dropdown transfer placement="right-start" v-if="menu.children" @on-click="dropdownClick">
                            <Button style="width: 85px;margin-left: -5px;padding:10px 0;" type="text">
                                <Icon :size="25" color="#fff" :type="menu.icon"></Icon>
                            </Button>
                            <DropdownMenu style="width: 200px;" slot="list">
                                <template v-for="(child, i) in menu.children">
                                    <DropdownItem :name="child.name">
                                        <div style="display:flex;align-items:center;">
                                            <Icon :size="16" :type="child.icon"></Icon>
                                            <span style="padding-left:10px;">
                                                {{ child.title }}
                                            </span>
                                        </div>
                                    </DropdownItem>
                                </template>  
                            </DropdownMenu>
                        </Dropdown>
                        <Dropdown transfer v-if="!menu.children && menu.showInMenus" placement="right-start" @on-click="dropdownClick">
                            <Button style="width: 85px;margin-left: -5px;padding:10px 0;" type="text">
                                <Icon :size="25" color="#fff" :type="menu.icon"></Icon>
                            </Button>
                            <DropdownMenu style="width: 200px;" slot="list">
                                <DropdownItem :name="menu.name">
                                    <div style="display:flex;align-items:center;">
                                        <Icon :size="16" :type="menu.icon"></Icon>
                                        <span style="padding-left:10px;">
                                            {{ menu.title }}
                                        </span>
                                    </div>
                                </DropdownItem>
                            </DropdownMenu>
                        </Dropdown>
                    </template>         
                </div>            
            </Sider>
            <Layout>
                <Header :style="{position: 'fixed',
                        width: isCollapsed?'calc(100% - 78px)':'calc(100% - 200px)',
                        padding: 0,
                        display:'flex',
                        flexDirection:'column',
                        zIndex:20
                    }" class="layout-header-bar">
                    <div style="
                        display:flex;
                        align-items:center;
                        justify-content:space-between;
                        position: relative;
                        height:60px;
                        line-height: 60px;
                        z-index: 1;
                        box-shadow: 0 2px 1px 1px rgba(100, 100, 100, 0.1);">
                        <div style="display:flex;align-items:center;">
                            <Icon @click.native="collapsedSider" :class="rotateIcon" :style="{margin: '0 20px 0'}" type="ios-menu" size="24"></Icon>
                            <span style="font-size:18px;font-weight:bold">后台管理系统</span>
                            <span style="font-size:14px;padding-left: 20px;">欢迎光临！ {{current_user}}</span>
                        </div>
                        <div style="margin-right:20px">
                            <Button type="text" icon="ios-apps" size="large" @click="enter_functions">进入功能区</Button>
                            <Button type="text" icon="ios-exit" size="large" @click="quit">退出系统</Button>
                        </div>
                    </div>     
                    <div style="display: flex;
                                position: relative;
                                padding-left:10px;
                                height: 40px;
                                background: #f5f7f9;
                                align-items: center;
                                box-shadow: 0 2px 1px 1px rgba(100, 100, 100, 0.1);">
                        <template v-for="(tab,tab_index) in tags">
                            <Tag type="dot" 
                            :closable="tab.closable" 
                            :color="tab.choosed ? '#00ff00':'#e9eaec'"
                            :name="tab.name"
                            @click.native="clickTag(tab)"
                            @on-close="closeTag" >
                                {{tab.title}}
                            </Tag>
                        </template>
                    </div>                  
                </Header>                
                <Content :style="{
                    height: 'calc(100% - 100px)',
                    position: 'absolute',
                    top: '100px',
                    overflow: 'auto',
                    padding: '10px',
                    width:isCollapsed?'calc(100% - 78px)':'calc(100% - 200px)'
                    }">
                    <!--保存组件状态到内存，避免重新渲染-->
                    <keep-alive>
                        <router-view/>    
                    </keep-alive>               
                </Content>
            </Layout>
        </Layout>
    </div>
  </section>
</template>
<script>
import {mapActions,mapState} from 'vuex'
import w_logo from '@/assets/images/logo.png'
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "Main",
    data(){
        return {
            logo: '',
            isCollapsed: false,
            title: "首页",
            activeMenuName: "dashboard",
            openMenuName: [],
            current_user: "",
            menus: []
        }
    },
    created: function() {
        this.$http.get(baseAPIUrl + "main_menu").then(response => {
            this.menus = response.data;

            let activeMenuName = localStorage.activeMenuName;
            this.activeMenuName = activeMenuName;
            var tags_last_num = 1;
            if(this.tags.length != 0)
                tags_last_num = this.tags[this.tags.length - 1].num; 

            if(activeMenuName && activeMenuName.length != 0){
                this.menus.forEach(_menu=>{
                    if(activeMenuName == _menu.name){                        
                        _menu.choosed = true;
                        _menu.showInTags = true;
                        _menu.num = tags_last_num + 1;
                    }
                    else if(_menu.children){
                        _menu.children.forEach(child=>{
                            if(activeMenuName == child.name){
                                child.choosed = true;
                                child.showInTags = true;
                                child.num = tags_last_num + 1;
                                this.openMenuName = [_menu.name];      
                            }
                        })                 
                    }
                    else{
                        // 排除首页
                        if(_menu.name != 'dashboard'){
                            _menu.choosed = false;
                            _menu.showInTags = false;
                        }else{
                            _menu.choosed = false;
                        }
                    }
                })
            }
            this.$nextTick(()=>{
                this.$refs.side_menu.updateOpened();
                this.$refs.side_menu.updateActiveName();
            }); 
        }, response => {
          this.$Message.error('请登陆');
          this.$router.push({
            name: "login"
          });
          return
        });
        this.logo = w_logo;
        this.$http.get(baseAPIUrl + "api/user").then(response => {
            this.current_user = response.data["name"];
        }, response => {
          this.$router.push({
            name: "login"
          });
        });
    },
    computed: {
        // ...mapState(
        //     {
        //         user:state=>state.user
        //     }
        // ),
        // 筛选menus中选中的menu
        tags(){
            let tags = [];
            // 将menus中showInTags=true的标签放到tags数组中
            this.menus.forEach(menu=>{
                if(menu.showInTags){
                    tags.push(menu);
                }else if(menu.children){
                    menu.children.forEach(child=>{
                        if(child.showInTags){
                            tags.push(child)
                        }
                    })
                }
            });
            //标签数组排序，从小到到
            tags.sort((a,b)=>{
                return (a.num - b.num)
            })
            return tags;
        },
        rotateIcon () {
            return [
                'menu-icon',
                this.isCollapsed ? 'rotate-icon' : ''
            ];
        },
        menuitemClasses () {
            return [
                'menu-item',
                this.isCollapsed ? 'collapsed-menu' : ''
            ]
        }
    },
    methods: {
        // ...mapActions([
        //     'logout'
        // ]),
        quit(){
            this.$http.get(baseAPIUrl + "logout").then(response => {
              this.$Message.success('退出成功！' + response.data.message);
              this.$router.push({
                name: "login"
              });
            }, response => {
              // this.$Message.error('请登陆');
            });
        },
        enter_functions(){
            this.$router.push({
                name: "index"
              });
        },
        collapsedSider() {
            this.$refs.side1.toggleCollapse();
        },
        // ------------------------------  菜单操作开始  --------------------------------
        closeTag(event, name){
            // 判断该标签是否是选中状态
            // 如果是那么就要设置标签数组中最后一个标签成选中状态
            // 如果否那么就直接删除就好
            let is_choosed = false;
            this.menus.forEach((menu,_index)=>{
                if(menu.name == name){
                    is_choosed = menu.choosed;
                    menu.showInTags = false;
                }else if(menu.children){
                    menu.children.forEach(child=>{
                        if(child.name == name){
                            is_choosed = child.choosed;
                            child.showInTags = false;
                        }
                    })
                }
            })          
            // 关闭标签并选中tags中最后一个标签高亮  
            if(is_choosed){
                let last_tag = this.tags[this.tags.length-1];
                last_tag.choosed = true;
                this.$router.push(last_tag.href);
                this.activeMenuName = last_tag.name;
                localStorage.activeMenuName = this.activeMenuName;
            }            
        },
        clickTag(tag){
            this.tags.forEach(_tag=>{
                if(_tag.name == tag.name){
                    _tag.choosed=true;
                }else{
                    _tag.choosed= false;
                }
            })
            // 设置菜单选中name
            this.activeMenuName = tag.name;
            localStorage.activeMenuName = this.activeMenuName;
            // 刷新菜单
            this.$nextTick(()=>{
                if(this.$refs.side_menu){
                    this.$refs.side_menu.updateActiveName()
                }
            });
            //点击tab跳转
            this.$router.push(`${tag.href}`);
        },
        choosedMenu(name){
            // 获取标签数组最后一个元素的num
            let tags_last_num = this.tags[this.tags.length - 1].num;
            // 设置选中菜单name
            this.activeMenuName = name;
            localStorage.activeMenuName = this.activeMenuName;
            let if_tab = false;

            //根据name查找对应的菜单对象
            let menu = null;
            this.menus.forEach(_menu=>{
                if(_menu.name == name){   
                    // 只有不在tags数组中的元素才能设置num                 
                    if(!_menu.showInTags){                   
                        _menu.num = tags_last_num + 1;
                    }
                    menu = _menu;
                    _menu.showInTags = true;
                    _menu.choosed = true;                
                                        
                }
                else if(_menu.children){
                    _menu.children.forEach(child=>{
                        if(child.name == name){     
                            // 只有不在tags数组中的元素才能设置num                       
                            if(!_menu.showInTags){
                                child.num = tags_last_num + 1; 
                            }            
                            menu = child;                
                            child.showInTags = true;
                            child.choosed = true;
                            
                        }else{
                            child.choosed = false;
                        }
                    })
                }
                else {
                    _menu.choosed = false;
                }
            })
            this.$router.push(`${menu.href}`);
        },
        dropdownClick(name){
            this.choosedMenu(name);
        }
        // ------------------------------  菜单操作结束  --------------------------------
    }
}
</script>
