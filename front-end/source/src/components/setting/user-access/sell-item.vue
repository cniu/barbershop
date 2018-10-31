<template>
    <Row>
        <Form ref="singleItem" :model="singleItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="单号" prop="item" style="display: none;">
                <Input disabled v-model="singleItem.item_number"></Input>
            </FormItem>
            <FormItem label="登陆用户" prop="username">
                <Input v-model="singleItem.username" placeholder="请输入登陆用户名称（譬如手机号）"></Input>
            </FormItem>
            <FormItem label="登陆密码" prop="password">
                <Input v-model="singleItem.password" type="password" placeholder="请输入登陆密码"></Input>
            </FormItem>
            <FormItem label="权限级别" prop="page_level">
                <InputNumber v-model="singleItem.page_level" :max=5 :min=1 placeholder="请输入权限级别"></InputNumber>
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
    name: "SellItem",
    props: {
        modal_type: '',
        singleItem: {
            username: '',
            password: '',
            page_level: '',
            comment: '',
            item_number: ''
        }
    },
    data() {
        return {
            ruleValidate: {
                username: [
                    { required: true, message: '请输入名称' }
                ],
                password: [
                    { required: true, message: '请输入密码' }
                ],
                page_level: [
                    { required: true, message: '请输入级别'},
                    { type: 'number', message: '错误金额'}
                ],
                comment: [
                    { required: false, message: '请输入备注', trigger: 'blur' },
                    { type: 'string', max: 200, message: '太长不易读', trigger: 'blur' }
                ]
            }
        }
    },
    methods: {
        handleSubmit (name) {
            this.$refs[name].validate((valid) => {
                if (valid) {
                    if(this.$props.modal_type == "modify"){

                        var post_URL = baseAPIUrl + "setting/user/" + this.singleItem.item_number;

                        this.$http.put(post_URL, this.singleItem).then(response => {
                            const res = response.data;
                            if(res['status'] != "success")
                                this.$Message.error(res['message']);

                            this.$Message.success('修改成功!');
                            this.$emit('closeModal', 'submit');
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
                        var post_URL = baseAPIUrl + "setting/user/1";
                        this.$http.post(post_URL, this.singleItem).then(response => {
                            const res = response.data;
                            if(res['status'] != "success")
                                this.$Message.error(res['message']);

                            this.$Message.success('新增成功!');
                            this.$emit('closeModal', 'submit');
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