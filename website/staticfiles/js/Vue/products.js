const productsSite  = new Vue({
        delimiters: ['[[', ']]'],
        el: '#productsSite',
        data: {
            errors: [],
            finalListEncoded:{data:[]},
            finalListDecoded:[],
            showOptionProducts: false,

            //filter bar
            filterByVal: "",
            componentLoaded: false
      },
        mounted(){
            //filter bar
            let selected = sessionStorage.getItem('filterBy');
            if(selected === null){
                selected = "";
            } else{
                this.filterByVal = selected;
            }

            this.componentLoaded = true;
        },
        methods: {
            //filter bar
             changePositionSelect(selected){
                const filterOption = document.querySelector('#filterBy');
                for (let key in filterOption) {
                    if(filterOption.hasOwnProperty(key)){
                        if (filterOption[key].value === selected){
                            filterOption[0].parentNode.insertBefore(filterOption[key], filterOption[0]);
                        }
                    }
                }
            },
          onChangeFilter(evt){
              sessionStorage.setItem('filterBy', evt.target.value);
              this.$refs.filterBySelect.submit();
            },
            //end filter bar
            findDuplicateEntry(articleSplit, productValue){
                //dict to push
                let dict = {article: articleSplit, quantity: productValue};

                //find occurrence
                let objFound = this.finalListEncoded.data.find(x => x.article === articleSplit);
                if(objFound === undefined){
                    this.finalListEncoded.data.push(dict);
                } else {
                    //change qty
                    objFound.quantity = productValue;
                }
                this.finalListDecoded = JSON.stringify(this.finalListEncoded.data);
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
            range(start, end, length = end - start + 1){
                 return Array.from({ length }, (_, i) => start + i)
            },
            // dropdown products
            toggleOptionProducts(){
              this.showOptionProducts = !this.showOptionProducts;

              // hide submenu on close
              if(!this.showOptionProducts){
                  const range = this.range(1, 10);
                  for(let i = 1; i < range.length; i++){
                      let elem = `ul${i}`;
                      if(typeof(document.querySelector(`#${elem}`)) != 'undefined' && document.querySelector(`#${elem}`) != null){
                        document.querySelector(`#${elem}`).style.display = 'none';
                      }
                  }

              }

              setTimeout( () => {
                  this.showOptionProducts ? this.$refs.hamburgerProducts.innerHTML = 'clear' : this.$refs.hamburgerProducts.innerHTML = 'menu';
              }, 50)
            },

            toggleSubmenuOptionProducts (ref)  {
                this.$refs[ref].style.display === "block" ? this.$refs[ref].style.display = "none" : this.$refs[ref].style.display = "block" ;
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
            regexId(article){
                return article.replace(/&nbsp;/g, '');
            },
      }
    });