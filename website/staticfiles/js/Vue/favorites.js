const favoritesSite  = new Vue({
        delimiters: ['[[', ']]'],
        el: '#favoritesSite',
        data: {
            errors: [],
            showModalDelete: false,
            loading: true,
            finalListEncoded:{data:[]},
            finalListDecoded:[]
      },
        computed(){

        },
        created(){this.findPosition()},
        beforeMount(){},
        mounted(){},

        methods: {
            toggleModalDelete(evt){
                this.loading = true;

                this.showModalDelete = !this.showModalDelete;
                  const target = evt.currentTarget;
                  setTimeout( () => {
                      document.querySelector("#deleteMsg").innerHTML = target.dataset.message;
                      document.querySelector('#deleteModalForm').action = target.dataset.url;
                  }, 100);
            },
            keepPosition(){
                sessionStorage.setItem('scrollCartPosition', window.scrollY.toString());
            },
            findPosition(){
                let scrollPosition = sessionStorage.getItem('scrollCartPosition');
                if (scrollPosition) window.scrollTo(0, parseInt(scrollPosition));
            },
            buildObjFavoritesToCart(article){
                //get data
                let product = this.$refs[article];
                // regex
                let articleSplit = this.regexId(article);

                //decode and populate this.finalListDecoded
                this.findDuplicateEntry(articleSplit, product.value);

            },
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

                    //remove obj if qty is 0
                    if(productValue == 0){
                        this.finalListEncoded.data = this.finalListEncoded.data.filter((value, index, arr) =>{
                            return value !== objFound;
                        });
                    }
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
            async addFavoritesToCart(evt){
                let url = evt.target.dataset.url;

                //list empty
                if(this.finalListDecoded.length <= 0){
                    //chge msg
                    this.$refs.favoritesDiv.innerHTML = '<i class="material-icons">clear</i>'+
                                                            '<span>Ajustez plusieurs quantités de favoris!</span>';
                    //revert msg
                    setTimeout(()=>{
                        this.$refs.favoritesDiv.innerHTML = '<i class="material-icons">add_shopping_cart</i>'+
                                                            '<span>Ajouter plusieurs favoris</span>';
                    }, 2500)

                }else{
                    //api
                    let response = await this.postApi(this.finalListDecoded, url);
                    if(response.status === 200){
                        this.$refs.favoritesDiv.innerHTML = '<i class="material-icons">done</i>'+
                                                            '<span>Favoris ajoutés</span>';
                    }else{
                        window.location.href = "/favorites";
                    }
                }
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
                return article.replace(/&nbsp;|,/g, '');
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
            }
      }
    });