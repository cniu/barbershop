<template>
    <Row>
        <Form ref="singleItem" :model="singleItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="单号" prop="item" style="display: none;">
                <Input disabled v-model="singleItem.item_number"></Input>
            </FormItem>
            <FormItem label="卡类型" prop="card_type_name">
                <Input style="width: 180px;" v-model="singleItem.card_type_name" placeholder="请输入卡类型名称"></Input>
            </FormItem>
            <FormItem label="打折比率" prop="discount">
                <InputNumber style="width: 180px;" v-model="singleItem.discount" :max="1" :min="0" :step="0.1" placeholder="请输入比率"></InputNumber>
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
const baseAPIUrl = process.env.baseAPIUrl;
export default {
    name: "SellItem",
    props: {
        modal_type: '',
        singleItem: {
            card_type_name: '',
            discount: 0,
            comment: '',
            item_number: ''
        }
    },
    data() {
        return {
            ruleValidate: {
                card_type_name: [
                    { required: true, message: '请输入名称' }
                ],
                discount: [
                    { required: true, message: '请填写折扣' }
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

                        var post_URL = baseAPIUrl + "setting/fellow_type/" + this.singleItem.item_number;

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
                        // var post_URL = baseAPIUrl + "sell_item/1";
                        // this.singleItem.item_type = this.singleItem.item_type.join(",");
                        // this.$http.post(post_URL, this.singleItem).then(response => {
                        //     const res = response.data;
                        //     if(res['status'] != "success")
                        //         this.$Message.error(res['message']);

                        //     this.$Message.success('新增成功!');
                        //     this.$emit('closeModal', 'submit');
                        // }, response => {
                        //     if(response.status == 401){
                        //       // this.$Message.error('请登陆');
                        //       this.$router.push({
                        //         name: "login"
                        //       });
                        //     }
                        // });
                    }
                } else {
                    this.$Message.error('请查看是否填写完必须输入的项!');
                }
            })
        },
        handleReset (name) {
            this.$refs[name].resetFields();
        },
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