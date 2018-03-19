/*
MugShot JQuery Plugin
version 1.0 March 11, 2018
by Cameron Nicolson
*/

(function($) {

	// Constructor function for MugShot Object
    function MugShot(element, options) {
    	if (element.id) window[element.id] = this;
        this.id = element.id;
    	this.element = $(element);
    	// the options value holds the updated defaults value
        this.options = $.extend({}, this.defaults, options);

        this._init();
    }

    MugShot.prototype = {

    	options: {},

		// holds the current roundSlider element
        element: null,

    	defaults: {
    		board: '643170459222980929',
    		token: 'AaJQ-l6vxCcM5KUNTNeY9yVHEPd4FRtUjoMUJzZExS3SeYAzEgAAAAA',
    		creator: null,
    		url: null,
    		note: null
    	},

    	_init: function() {
    		this._getMugPhoto();
    		this._render();
    	},

    	_render: function() {
    		this.container = this.$createElement("div.mugshot-container");
            this.innerContainer = this.$createElement("div.mugshot-inner-container");
            this.imgElem = this.$createElement("img.mugshot-img img").attr('src', '/static/src/img/ajax-loader.gif');
            this.container.append(this.innerContainer.append(this.imgElem));
            this.element.addClass("mugshot-control").empty().append(this.container);
    	},

    	_getMugPhoto: function() {
    		var self = this;
    		url = "https://api.pinterest.com/v1/boards/643170459222980929/pins/?access_token=AaJQ-l6vxCcM5KUNTNeY9yVHEPd4FRtUjoMUJzZExS3SeYAzEgAAAAA&fields=id%2Clink%2Curl%2Cimage%2Coriginal_link%2Cnote"
		    $.get(url, function(res, status){
		    	items = res.data
				$.each(items, function(i, item) {
				    self.creator = item.id, self.url = item.image.original.url,
				    self.note = item.note;
				});
		    	console.log(res);
		    	if(status === 'success') self._updateDisplay();
		    });
    	},

    	_updateDisplay: function() {
    		$(this.imgElem).attr("src", this.url);
    	},

    	// common core method
        $createElement: function(tagName){
        	console.log(tagName);
        	var t = tagName.split('.');
	    	return $( document.createElement(t[0])).addClass(t[1] || '');
        },

    }

  $.fn.mugshot = function(options) {
  	return this.each(function(){
	    var element = $(this);

	    // Return early if this element already has a plugin instance
	    if (element.data('mugshot')) return element.data('mugshot');

	    // The plugin initialization
	    // passes options to plugin constructor
	    var mugshot = new MugShot(this, options, arguments);

	    // Store plugin object in this element's data
	    element.data('mugshot', mugshot);

    });
  };

})(jQuery);