        const Home  = new Vue({
      delimiters: ['[[', ']]'],
      el: '#homeAts',
      props:{},
      data: {
              showModalCondition: false,
              title: "test",
              bodyCondition: null,
              loading: true,
              errors:[],
              serverSuccess: false,
              serverError: false,
              currentURL:window.location.href,

      },
        computed: {
          },
        mounted() {
        },
      methods: {
          toggleModalCondition (evt, title) {
              let url = evt.target.dataset.url;
              this.loading = true;
              this.title = title;
              this.callApi(url).then( (response) =>{
                  this.bodyCondition = decodeURIComponent(JSON.parse(response.data)).replaceAll('', '<br/>.');
                    this.loading = false;
              } );
              this.showModalCondition = !this.showModalCondition;
          },
          async callApi(url) {
              const headers = {'Content-Type': 'application/json', 'charset': 'utf-8'};
              return await axios.get(url, headers);

          },
          async addToCart(evt){
                //dataset data
                let url = evt.target.dataset.url;
                let id = evt.target.dataset.id;
                //get input quantity
                let product = this.$refs[id];
                //build dict
                let data = {"quantity": product.value}
                //response
                let response = await this.postApi(data, url);

                //chge icon depends on status received
                let icon = `f_${id}`

                if(response.status === 200) {
                    //set cart length in local storage
                    this.setLengthCart(response.data.cartLength);
                }

                //change material icon button
                this.$refs[icon].innerHTML = response.data.msg;
            },
          async postApi(data, url) {
              if(data){
                  let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
                  return axios({
                      method : "POST",
                      url,
                      headers: {'X-CSRFTOKEN': token, 'Content-Type': 'application/json'},
                      data: data
                  })
              } else {
                  return await axios.get(url)
              }
          },
          setLengthCart(len){
                //set local storage
                localStorage.setItem("cartLength", len);

                //create event to get it in navbar
                window.dispatchEvent(new CustomEvent('cartLengthLocalstorageChanged', {
                  detail: {
                    storage: localStorage.getItem('cartLength')
                  }
                }));
            },
      }
    });