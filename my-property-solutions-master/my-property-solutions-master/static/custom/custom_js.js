function name(deal_id, lead_id){
  $.ajax({
    url: "/dashboard/deals/" + deal_id + "/renovation-details/confirm",
    type: "GET",
    contentType: "application/json",
    dataType: "json",
    success: function(data, status, xhr) {
      if (data['status'] == 'alert') {
        alert("Please Go To The Offer Details/Purchase and click-->Submit");
      }
      if (data['status'] == 'redirect') {
        window.location.href = '/dashboard/deals/' + deal_id + '/renovation-details';
      }
    },
    error: function(data, status, xhr) {
      alert("Some error occured. Please try again!");
    },
  });
}

$(".ve-sh-number-js").children().on("keyup", function(event) {
  var value = $(this).val();
  if(event.which >= 37 && event.which <= 40){
    event.preventDefault();
  }
  var num = value.replace(/[\,\A-Za-z]/g, '');
  $(this).val(num.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,"));
});