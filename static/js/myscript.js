
   
//    $('.plus-cart').click(function(){
//     // console.log(" button click")
//     // console.log(this.parentNode)
//     // console.log(this.parentNode.children[2])
//     var id=$(this).attr("pid").toString();
//     var eml = this.parentNode.children[2]
//     console.log("pid =",id)
//     $.ajax({
//         type:"GET",
//         url:"/pluscart",
//         data:{
//             service_id:id
//         },
//         success:function(data){
//             console.log("data =",data)
//             console.log("success")
//             eml.innerText=data.service_qty
//             document.getElementById("amount").innerText=data.amount
//             document.getElementById("totalamount").innerText=data.totalamount


//         }
//     })
     

//    })