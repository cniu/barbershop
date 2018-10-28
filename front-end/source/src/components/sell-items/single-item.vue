<template>
    <Row>
        <Form ref="singleItem" :model="singleItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="发型师" prop="hairdresser">
                <Select v-model="singleItem.hairdresser" placeholder="请选择发型师">
                    <Option v-for="(option, index) in hairdresser_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem label="助理" prop="assistant">
                <Select v-model="singleItem.assistant" placeholder="请选择助理">
                    <Option v-for="(option, index) in assistant_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem label="消费类型" prop="item_type">
                <CheckboxGroup v-model="singleItem.item_type">
                    <Checkbox label="染发"></Checkbox>
                    <Checkbox label="烫发"></Checkbox>
                    <Checkbox label="假发"></Checkbox>
                    <Checkbox label="洗头"></Checkbox>
                </CheckboxGroup>
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
                    <Col span="13">
                        <Select
                            v-model="singleItem.fellow" style="width: 180px;"
                            filterable>
                            <Option v-for="(option, index) in fellow_list" :value="option.value" :key="index">{{option.label}}</Option>
                        </Select>
                    </Col>
                    <Col span="3">余额：</Col>
                    <Col span="8">
                        <Input v-model="fellow_rest" disabled placeholder="0" />
                    </Col>
                </Row>                
            </FormItem>
            <FormItem label="备注" prop="comment">
                <Input v-model="singleItem.comment" type="textarea" :autosize="{minRows: 2,maxRows: 5}" placeholder="可以输入备注以便记录"></Input>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="handleSubmit('singleItem')">Submit</Button>
                <Button @click="handleReset('singleItem')" style="margin-left: 8px">Reset</Button>
            </FormItem>
        </Form>
    </Row>
</template>
<script>
export default {
    name: "SingleItem",
    props: {
        hairdresser_list: [],
        assistant_list: [],
        fellow_list: [],
        singleItem: {
            hairdresser: '',
            assistant: '',
            item_type: '',
            money: '',
            pay_type: [],
            fellow: '',
            comment: ''
        }
    },
    data() {
        return {
            ruleValidate: {
                hairdresser: [
                    { required: true, message: '请选择发型师' }
                ],
                assistant: [
                    { required: true, message: '请选择助理' }
                ],
                pay_type: [
                    { required: true, message: '请选择付款类型' }
                ],
                money: [
                    { required: true, message: '请填写金额' },
                    { type: 'number', message: '错误金额'}
                ],
                item_type: [
                    { required: true, type: 'array', message: '请选择消费类型' }
                    // { type: 'array', max: 2, message: 'Choose two hobbies at best' }
                ],
                fellow: [
                    { required: false, message: '请输入会员手机号' }
                ],
                comment: [
                    { required: false, message: '请输入备注', trigger: 'blur' },
                    { type: 'string', max: 200, message: '太长不易读', trigger: 'blur' }
                ]
            }
        }
    },
    created: {

    },
    methods: {
        handleSubmit (name) {
            console.log(this.singleItem);
            this.$refs[name].validate((valid) => {
                if (valid) {
                    this.$emit('closeModal', 'submit');
                    this.$Message.success('Success!');
                } else {
                    this.$Message.error('请重新输入!');
                }
            })
        },
        handleReset (name) {
            this.$refs[name].resetFields();
        },
        getFellowList (query) {
            // if (query !== '') {
            //     this.fellow_loading = true;
            //     setTimeout(() => {
            //         this.fellow_loading = false;
            //         const list = this.list.map(item => {
            //             return {
            //                 value: item,
            //                 label: item
            //             };
            //         });
            //         this.fellow_list = list.filter(item => item.label.toLowerCase().indexOf(query.toLowerCase()) > -1);
            //     }, 200);
            // } else {
            //     this.fellow_list = [];
            // }
        }
    }
}
</script>