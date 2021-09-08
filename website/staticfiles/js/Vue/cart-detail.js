 const cart  = new Vue({
        delimiters: ['[[', ']]'],
        el: '#cartAts',
        data: {
            errors: [],
            filterByVal: "",
            componentLoaded: false,
            totalWithTaxes:0,
            totalWithoutTaxes:0,
            showModalConfirmCart: false,
            showModalLeaveMsg: false,
            messageOrder: null,
            checked : false,
            url: "#",
            deliveryChoice:false,
            showModalPaymentCondition: false,
            bodyPaymentCondition: null,
            loading: true,
            sendOrder: false,
            success_msg: "",
            err_msg: "",
            currentURL: window.location.href,
            serverSuccess: false,
            serverError: false,
            loadingMsg: false,

            //totalJoin for CB
            total:0,
            userConnected: false,
            harborCeilingsDrive:0,
            harborCeilingsDelivery:0

      },
        computed(){

        },
        created(){},
        beforeMount(){},
        mounted(){
            this.findPosition();
            this.total = (this.$refs.totalCart.value).replace(/&nbsp;/g, '');
            this.harborCeilingsDrive = parseInt(this.$refs.harborCeilingsDrive.value);
            this.harborCeilingsDelivery = parseInt(this.$refs.harborCeilingsDelivery.value);
            this.$refs.userConnected.value === "True" ? this.userConnected = true : this.userConnected = false;
            },

        methods: {
            // show general condition modal
            toggleModalGeneralConditions(){
                this.showModalConfirmCart = !this.showModalConfirmCart;
            },

            // show order msg modal
            toggleModalLeaveAMessage(){
                this.showModalLeaveMsg = !this.showModalLeaveMsg;
            },

            // show payment condition modal
            togglePaymentConditionModal(evt){
                this.loading = true;
                this.showModalPaymentCondition = !this.showModalPaymentCondition;
                let url = evt.target.dataset.url;
                this.callApi(false, url).then(response => {
                        this.bodyPaymentCondition = decodeURIComponent(JSON.parse(response.data)).replaceAll('', '<br/>.');
                        this.loading = false;
                }).catch(() => {
                    this.bodyPaymentCondition = "En attente de conditions"
                });
            },
          async onChangeFilter(evt){
              let url = evt.target.dataset.url;
             this.callApi(evt.target.value, url)
                 .then(response => {
                     if(response.status === 200){
                         this.deliveryChoice = true;
                     }
                }).catch((e)=>{

                 console.log(e);
                 window.location.href = '/';
              });
            },
            async callApi(data, url) {
              if(data){
                  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
                  return axios({
                      method : "POST",
                      url,
                      headers: {'X-CSRFTOKEN': token, 'Content-Type': 'application/json'},
                      data: {"data": data}
                  })
              } else {
                  return await axios.get(url)
              }

          },
            keepPosition(){
                sessionStorage.setItem('scrollCartPosition', window.scrollY.toString());
            },
            findPosition(){
                let scrollPosition = sessionStorage.getItem('scrollCartPosition');
                if (scrollPosition) window.scrollTo(0, parseInt(scrollPosition));
            },
            //handle onChange input qty
            async checkValue(ref, refLine){
                //get value changed
                const value = parseFloat(ref.target.value);

                //if value === 0 reload page
                if(value === 0){
                    this.keepPosition();
                    window.location.assign("/cart");
                }

                //get product changed
                const article = ref.target

                //get unit price
                const unitPrice = parseFloat(refLine.dataset.unit)

                //chge value line of the product
                refLine.innerHTML = (value * unitPrice).toFixed(2)

                //get total cart ref
                const totalCart = this.$refs.totalCart



                let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
                //sendData
                let response = await this.sendUpdateCart('/cart/update/', token, {
                    'article_id': refLine.dataset.id,
                    'quantity': value
                });

                //success
                if(response.status === 200){

                    //chge value total cart
                    this.total = `${response.data['total']}`;
                }
            },
            async checkFormLeaveMsg(e) {
              let url = e.target.dataset.url;
              let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
              if (this.messageOrder) {
                    this.loadingMsg = true;
                    let response = await this.sendMsg(url, token);
                    this.serverSuccess = true;
                    this.success_msg = response.data['msg'];
                    if(response.status === 200){
                        setTimeout(()=>{
                            this.showModalLeaveMsg = false;
                            this.serverSuccess = false;
                            this.loadingMsg = false;
                        }, 1000)

                    } else {
                        this.loadingMsg = false;
                          this.serverError = true;
                          this.err_msg = response.data['err'];
                          setTimeout(() => {
                              this.serverError = false;
                          }, 2000)
                    }
              }

              if (!this.messageOrder) {
                this.errors.push('Message requis');
              }

            },
          async sendMsg(url, token) {
                this.success_msg = "";
                this.err_msg = "";

             return await axios({
                    method : "POST",
                    url:url, //django path name
                    headers: {'X-CSRFTOKEN': token, 'Content-Type': 'application/json'},
                    data : {"data":this.messageOrder},//data
                  })
          },
            async sendUpdateCart(url, token, data) {
                this.success_msg = "";
                this.err_msg = "";

             return await axios({
                    method : "POST",
                    url:url, //django path name
                    headers: {'X-CSRFTOKEN': token, 'Content-Type': 'application/json'},
                    data : data,//data
                  })
          },

      }
    });