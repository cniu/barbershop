<template>
    <Row>
        <Form ref="singleItem" :model="singleItem" :rules="ruleValidate" :label-width="80">
            <FormItem label="单号" prop="item" style="display: none;">
                <Input disabled v-model="singleItem.item_number"></Input>
            </FormItem>
            <FormItem label="类型" prop="flow_direction">
                <RadioGroup v-model="singleItem.flow_direction">
                    <Radio label="出账">出账</Radio>
                    <Radio label="入账">入账</Radio>
                </RadioGroup>
            </FormItem>
            <FormItem label="金额" prop="money">
                <InputNumber style="width: 180px;" v-model="singleItem.money" placeholder="请输入金额"></InputNumber>
            </FormItem>
            <FormItem label="条目类别" prop="item_type">
                <Select v-model="singleItem.item_type" placeholder="请选择条目类别">
                    <Option value="工资">工资</Option>
                    <Option value="房租">房租</Option>
                    <Option value="日常费用">日常费用</Option>
                    <Option value="其他">其他</Option>
                </Select>
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
const baseAPIUrl = process.env.baseAPIUrl
export default {
  name: 'AddFlow',
  props: {
    modal_type: '',
    employee_list: '',
    singleItem: {
      flow_direction: '',
      item_type: '',
      money: 0,
      created_by: '',
      item_number: '',
      comment: ''
    }
  },
  data () {
    return {
      ruleValidate: {
        flow_direction: [
          { required: true, message: '请选择'}
        ],
        item_type: [
          { required: true, message: '请选择类型' }
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
    handleSubmit (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          var post_URL = baseAPIUrl + 'handle_flow/single_item'

          this.$http.post(post_URL, this.singleItem).then(response => {
            const res = response.data
            if (res['status'] != 'success') { this.$Message.error(res['message']) } else {
              this.$Message.success('添加成功!')
              this.$emit('closeModal', 'submit')
              this.$refs[name].resetFields()
            }
          }, response => {
            if (response.status == 401) {
              // this.$Message.error('请登陆');
              this.$router.push({
                name: 'login'
              })
            }
          })
        } else {
          this.$Message.error('请查看是否填写完必须输入的项!')
        }
      })
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    }
  }
}
</script>
