const filterBar = new Vue({
        delimiters: ['[[', ']]'],
      el: '#filterBarAts',
      data: {
        events: [],
          value: 100,
          componentLoaded: false,
          choice:"All",
          products: []

      },
        mounted(){
            let value  = sessionStorage.getItem('value');
            if(value === null) value = 100
            let choice = sessionStorage.getItem('choice');
            if(choice === null ) choice = "All"
            this.value = value;
            this.choice = choice;
            this.componentLoaded = true;
        },
        computed: {
          total: function () {

          if(! this.componentLoaded){
              return null;
          } else {
              sessionStorage.setItem('value', this.value);
              sessionStorage.setItem('choice', this.choice);
              return this.value
          }

        },
            filteredPeople: function() {
                let vm = this;
                let vat = vm.selectedVAT;
                let data = JSON.parse(this.products)

                if (vat === "All") {
                    console.log('all', data)
                } else {
                    return data.filter((arg) => {
                        return arg.rate_VAT === rate_VAT;
                    });
                }
            }
      },
      methods: {
            addEvent ({ type, target }) {
          const event = {
              type,
              isCheckbox: target.type === 'checkbox',
              target: {
                value: target.value,
                checked: target.checked
              }
          };
            this.events.push(event)
        },
        eventText (e) {
            return `${e.type}: ${e.isCheckbox ? e.target.checked : e.target.value}`
            },
      },
      saveData(ref){
            console.log(ref)
      }
})