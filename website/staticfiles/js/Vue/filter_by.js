const filterBy  = new Vue({
        el: '#filterBy',
        data: {
            filterByVal: "",
            componentLoaded: false
      },
        mounted(){
            let selected = sessionStorage.getItem('filterBy');
            if(selected === null){
                selected = "";
            } else{
                this.filterByVal = selected;
            }

            this.componentLoaded = true;
        },

        methods: {
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
      }
    });