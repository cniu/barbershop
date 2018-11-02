<template>
    <Row>
        <Form ref="singleItem" :model="singleItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="单号" prop="item" style="display: none;">
                <Input disabled v-model="singleItem.item_number"></Input>
            </FormItem>
            <FormItem label="姓名" prop="name">
                <Input v-model="singleItem.name" placeholder="请输入姓名"></Input>
            </FormItem>
            <FormItem label="手机号" prop="phone_number">
                <InputNumber style="width: 280px;" disabled v-if="modal_type != 'add'" v-model="singleItem.phone_number" placeholder="请输入手机号"></InputNumber>
                <InputNumber style="width: 280px;" v-if="modal_type == 'add'" v-model="singleItem.phone_number" placeholder="请输入手机号"></InputNumber>
            </FormItem>
            <FormItem label="消费密码" prop="password">
                <Input v-model="singleItem.password" type="password" placeholder="请设置消费密码"></Input>
            </FormItem>
            <FormItem label="生日" prop="birthday">
                <DatePicker v-model="singleItem.birthday" type="date" placeholder="Select date" style="width: 200px"></DatePicker>
            </FormItem>
            <FormItem label="卡类型" prop="card_type">
                <Select v-model="singleItem.card_type" placeholder="请选择会员卡类型">
                    <Option v-for="(option, index) in card_type_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem label="余额" prop="money">
                <InputNumber style="width: 180px;" v-if="modal_type == 'add'" v-model="singleItem.money" placeholder="请输入金额"></InputNumber>
                <InputNumber style="width: 180px;" disabled v-if="modal_type != 'add'" v-model="singleItem.money" placeholder="请输入金额"></InputNumber>
            </FormItem>
            <FormItem label="开卡人" prop="created_by">
                <Select v-model="singleItem.created_by" placeholder="请选择开卡人">
                    <Option v-for="(option, index) in employee_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmit('singleItem')">提交</Button>
                <Button @click="handleReset('singleItem')" style="margin-left: 8px">重置</Button>
            </FormItem>
        </Form>
    </Row>
</template>
<script>
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "SellItem",
    props: {
        modal_type: '',
        card_type_list: '',
        employee_list: '',
        singleItem: {
            name: '',
            phone_number: '',
            birthday: '',
            card_type: '',
            money: 0,
            created_by: '',
            password: '',
            item_number: ''
        }
    },
    data() {
        return {
            ruleValidate: {
                name: [
                    { required: true, message: '请输入名称', trigger: "blur" }
                ],
                phone_number: [
                    { required: true, message: '请输入电话号码'},
                    { type: 'number', message: '错误格式'}
                ],
                birthday: [
                    { required: false, message: '请选择日期'},
                    // { required: false, type: 'date', message: '错误格式'}
                ],
                card_type: [
                    { required: true, message: '请选择卡类型' }
                ],
                money: [
                    { required: true, message: '请填写金额' },
                    { type: 'number', message: '错误金额'}
                ],
                created_by: [
                    { required: true, message: '请选择开卡人' }
                ]
            }
        }
    },
    methods: {
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if(this.$props.modal_type == "modify"){

                        var post_URL = baseAPIUrl + "fellow/" + this.singleItem.phone_number;

                        var temp = Object.assign({}, this.singleItem);
                        temp.birthday = temp.birthday.toString();
                        this.$http.put(post_URL, temp).then(response => {
                            const res = response.data;
                            if(res['status'] != "success")
                                this.$Message.error(res['message']);
                            else{
                                this.$Message.success('修改成功!');
                                this.$emit('closeModal', 'submit');
                                this.$refs[name].resetFields();
                            }
                        }, response => {
                            if(response.status == 401){
                              // this.$Message.error('请登陆');
                              this.$router.push({
                                name: "login"
                              });
                            }
                        });
                    }
                    else if(this.$props.modal_type == "add"){
                        var post_URL = baseAPIUrl + "fellow/1";

                        var temp = Object.assign({}, this.singleItem);
                        temp.birthday = temp.birthday.toString();
                        this.$http.post(post_URL, temp).then(response => {
                            const res = response.data;
                            if(res['status'] != "success"){
                                this.$Message.error(res['message']);
                            }
                            else{
                                post_URL = baseAPIUrl + "handle_flow/add_fellow";
                                this.$http.post(post_URL, {
                                    "money": this.singleItem.money,
                                    "fellow_phone_number": this.singleItem.phone_number
                                }).then(response => {
                                    const res = response.data;
                                    if(res['status'] != "success")
                                        this.$Message.error(res['message']);
                                }, response => {
                                });
                                this.$Message.success('新增成功!');
                                this.$emit('closeModal', 'submit');  
                                this.$refs[name].resetFields();    
                            }
                        }, response => {
                            if(response.status == 401){
                              // this.$Message.error('请登陆');
                              this.$router.push({
                                name: "login"
                              });
                            }
                        });
                    }
                } else {
                    this.$Message.error('请查看是否填写完必须输入的项!');
                }
            })
        },
        handleReset (name) {
            this.$refs[name].resetFields();
        }
    }
}
</script>