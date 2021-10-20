var notis = document.querySelectorAll('.noti')

if (notis){
  notis.forEach((noti) => {
      noti.addEventListener('click', () =>{
      noti.parentNode.removeChild(noti);
    })
  });


}
