//we create event handler for the each button ussing'update-cart'
//we first we query all the item in that class
var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    //for every button we add event listener like updatebtn[i]
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product //'this' is same as 'self' in python
		var action = this.dataset.action//here action is for productdetail.html data-action when we click add to basket it show its action
		console.log('productId:', productId, 'action:', action)
		console.log('USER:', user)
        // location.reload()
		if (user == 'AnonymousUser'){
            console.log('not log in')
			// addCookieItem(productId, action)
		}else{
            // console.log('user is loged in')

            //here we pass the productid and action to the function updateuserorder
			updateUserOrder(productId, action) //when user is authenticated
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

    var url = '/update_item/' 
    //console.log('URL:', url)

    fetch(url, {//fetch url from of updateitem function of views
        method:'POST',//make post request
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,//can have csrf toke  access we need to add hte cookei function in our main html page in the header file
        }, 
        //query data to productid in update item for productid and action
        body:JSON.stringify({'productId':productId, 'action':action})//send action and production to the views
    })
    .then((response) => {//to return the views-156 line response as a promise 
        return response.json();
    })
    .then((data) => {
        console.log('data:',data)
        location.reload()
    });
}

// //for guset user or unauthenticated user
// function addCookieItem(productId, action){
// 	console.log('User is not authenticated')

// 	if (action == 'add'){
// 		if (cart[productId] == undefined){
// 		cart[productId] = {'quantity':1}

// 		}
// 		else{
// 			cart[productId]['quantity'] += 1
// 		}
// 	}

// 	if (action == 'remove'){
// 		cart[productId]['quantity'] -= 1

// 		if (cart[productId]['quantity'] <= 0){
// 			console.log('Item should be deleted')
// 			delete cart[productId];
// 		}
// 	}
// 	console.log('CART:', cart) //add to cart for unauthorixe
// 	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
// 	location.reload()
// }
