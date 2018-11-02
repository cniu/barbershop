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
            <FormItem label="入职日期" prop="first_day">
                <DatePicker v-model="singleItem.first_day" type="date" placeholder="Select date" style="width: 200px"></DatePicker>
            </FormItem>
            <FormItem label="员工类型" prop="employee_type">
                <Select v-model="singleItem.employee_type" placeholder="请选择员工类别">
                    <Option v-for="(option, index) in employee_type_list" :value="option.value" :key="index">{{option.label}}</Option>
                </Select>
            </FormItem>
            <FormItem label="底薪" prop="base_salary">
                <InputNumber style="width: 180px;" :min="0" v-model="singleItem.base_salary" placeholder="请输入提成比率"></InputNumber>
            </FormItem>
            <FormItem label="提成比率" prop="percentage">
                <InputNumber style="width: 180px;" :max="1" :min="0" :step="0.1" v-model="singleItem.percentage" placeholder="请输入提成比率"></InputNumber>
            </FormItem>
            <FormItem label="状态" prop="status">
                <RadioGroup v-model="singleItem.status">
                    <Radio label="在职">在职</Radio>
                    <Radio label="离职">离职</Radio>
                </RadioGroup>
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
        employee_type_list: '',
        singleItem: {
            name: '',
            phone_number: '',
            first_day: '',
            employee_type: '',
            base_salary: 0,
            percentage: 0,
            status: '',
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
                first_day: [
                    { required: true, message: '请选择日期'},
                    // { required: false, type: 'date', message: '错误格式'}
                ],
                employee_type: [
                    { required: true, message: '请选择员工类型' }
                ],
                base_salary: [
                    { required: true, message: '请填写底薪' },
                    { type: 'number', message: '错误格式'}
                ],
                percentage: [
                    { required: true, message: '请填写提成比率' },
                    { type: 'float', message: '错误提成比率格式'}
                ],
                status: [
                    { required: true, message: '请选择状态', trigger: "blur" }
                ]
            }
        }
    },
    methods: {
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if(this.$props.modal_type == "modify"){

                        var post_URL = baseAPIUrl + "employee/" + this.singleItem.phone_number;

                        var temp = Object.assign({}, this.singleItem);
                        temp.first_day = temp.first_day.toString();
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
                        var post_URL = baseAPIUrl + "employee/1";

                        var temp = Object.assign({}, this.singleItem);
                        temp.first_day = temp.first_day.toString();
                        this.$http.post(post_URL, temp).then(response => {
                            const res = response.data;
                            if(res['status'] != "success")
                                this.$Message.error(res['message']);
                            else{
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