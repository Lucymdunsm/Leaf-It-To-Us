$( "#popular" ).on( "click", filter );
$( "#type" ).on( "click", filter );
$( "#origin" ).on( "click", filter );
$( "#atoz" ).on( "click", filter );

function filter(evt) {
	evt.preventDefault();
	if(evt.target.id == null) return;
	var endpoint
	if(evt.target.id != null) {
		endpoint = evt.target.id
	}
	var teaids = findTeaIds();
	url = '/leafittous/teas/'+endpoint+"/";

	$.ajax({
	  url: url,
	  type: 'POST',
	  data: JSON.stringify(teaids),
	  success: function(data){
	  	var receivedJson = JSON.parse(data);
	 	refresh_listview(receivedJson);
	  },
   		contentType: "application/json; charset=utf-8",
    	dataType: "json"
	});
}

function findTeaIds(selector) {
	var array = [];
	var found = {"tea_id": array};
	$(".filterable").find("[data-teaid]").each(function(i, item){ 
		array[i] = $(this).attr("data-teaid");
	});
	console.log(found);
	return found;
} 

function refresh_listview(json) {
	console.log(json)
	var $container = $("#catalog-list");
	$container.hide();
	var htmlNewList = '';
	$.each(json, function(i, item) {
		htmlNewList += '<a href="#" class="list-group-item" data-teaid="'+item.pk+'">'
		htmlNewList += '<span class="badge"> views '+ item.fields.views +'</span>'
		htmlNewList += '<h4 class="list-group-item-heading">' + item.fields.name + '</h4>'
		htmlNewList += '<p>'+ item.fields.description + '</p>'
 		htmlNewList += '</a>'
	});
	$container.html(htmlNewList).fadeIn();
}

$( ".score" ).each( function( index, element ){
	t = $(this).data("rating");
    for (var e = t, r = 0; r <= e; r++) {
    	$(this).find('span:nth-child(' + r + ')').addClass("checked");
    }
});