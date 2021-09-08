const searchBar  = new Vue({
      el: '#searchbar',
      data: {
            priceRangeValue: 50,
            events: []
      },
      methods: {
            getInfoOnClick (elem) {
                elem.submit();
            },
            getInfoOnKey (elem) {
                clearTimeout(this.timeout);
                this.timeout = setTimeout( () => {
                    elem.submit();
                }, 2000);
            },
        }
    });