<template>
    <Row>
        <Form ref="singleItem" :model="singleItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="单号" prop="item" style="display: none;">
                <Input disabled v-model="singleItem.item_number"></Input>
            </FormItem>
            <FormItem label="消费金额" prop="money">
                <InputNumber style="width: 180px;" v-model="singleItem.money" placeholder="请输入金额"></InputNumber>
            </FormItem>
            <FormItem label="付款类型" prop="pay_type">
                <RadioGroup v-model="singleItem.pay_type">
                    <Radio label="现金">现金</Radio>
                    <Radio label="微信">微信</Radio>
                    <Radio label="支付宝">支付宝</Radio>
                    <Radio label="刷卡">刷卡</Radio>
                </RadioGroup>
            </FormItem>
            <FormItem label="会员" prop="fellow">
                <Row>
                    <Col span="16">
                        <Select v-model="singleItem.fellow" style="width: 180px;" filterable>
                            <Option v-for="(option, index) in fellow_list" :value="option.value" :key="index" >{{option.label}}</Option>
                        </Select>
                    </Col>
                    <Col span="8">    
                        <Button type="primary" size="small" @click="showFellowInfo">查看会员信息</Button>
                    </Col>
                </Row>                
            </FormItem>
            <FormItem label="操作员" prop="created_by">
                <Select v-model="singleItem.created_by" placeholder="请选择操作员">
                    <Option v-for="(option, index) in employee_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem label="备注" prop="comment">
                <Input v-model="singleItem.comment" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="可以输入备注以便记录"></Input>
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
    name: "OtherItem",
    props: {
        modal_type: '',
        employee_list: '',
        fellow_list: '',
        singleItem: {
            fellow: '',
            pay_type: '',
            money: 0,
            created_by: '',
            item_number: '',
            comment: ''
        }
    },
    data() {
        return {
            ruleValidate: {
                fellow: [
                    { required: false, message: '请选择会员手机号'},
                ],
                pay_type: [
                    { required: true, message: '请选择支付方法' }
                ],
                money: [
                    { required: true, message: '请填写金额' },
                    { type: 'number', message: '错误金额'}
                ],
                created_by: [
                    { required: true, message: '请选择开卡人' }
                ],
                comment: [
                    { required: true, message: '请输入备注', trigger: 'blur' },
                    { type: 'string', max: 200, message: '太长不易读', trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        showFellowInfo () {
            const fellow_info = this.fellow_list.filter(item => item['value'] == this.singleItem.fellow);
            const content = 
                '<p>姓名：' + fellow_info[0]['name'] + '</p>' +
                '<p>卡类型：' + fellow_info[0]['card_type'] + '</p>' +
                '<p>余额：' + fellow_info[0]['money'] + '</p>' + 
                '<p>手机号：' + fellow_info[0]['value'] + '</p>';
            this.$Modal.success({
                title: "会员信息",
                content: content
            });
        },
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if(this.singleItem.pay_type != "刷卡" && this.singleItem.fellow != undefined){
                        this.$Modal.error({
                            title: '请确认是否填写正确',
                            content: '<p>若选会员，请选择刷卡类别</p>'
                        });
                        return false;
                    }
                    else if(this.singleItem.pay_type == "刷卡" && this.singleItem.fellow == undefined){
                        this.$Modal.error({
                            title: '请确认是否填写正确',
                            content: '<p>若选刷卡，请选择会员</p>'
                        });
                        return false;
                    }
                    var post_URL = baseAPIUrl + "handle_flow/other_item";

                    this.$http.post(post_URL, this.singleItem).then(response => {
                        const res = response.data;
                        if(res['status'] != "success")
                            this.$Message.error(res['message']);
                        else{
                            this.$Message.success('消费成功!');
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