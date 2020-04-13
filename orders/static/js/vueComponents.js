var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        tip_amount: 0,
        amounts: [],
        final_total: 0
    },
    created() {
      fetch('http://127.0.0.1:8000/add_tip_total/15')
          .then(response => response.json())
          .then(results=> this.amounts = results)

    },
      methods: {
          addTip: function () {
              this.final_total = Number(this.amounts.final_total) + Number(this.tip_amount)
              console.log(this.final_total)
              document.getElementById('text_total').innerText = Math.ceil(this.final_total*100)/100
          }
      }
})

