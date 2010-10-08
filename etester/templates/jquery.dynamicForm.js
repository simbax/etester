/*
 * jquery.dynamicForm.js
 * Arietis Software Innovations
 * version: 1.1
 * ----------------------------
 * distributed under the GNU General Public License 
 * which means that its source code is freely-distributed 
 * and available to the general public
 *
 * html structure:
 *
 * <form name="myform" id="myform" method="post" action="#">
 * 	<label>Team name: <input type="text" id="teamname" name="teamname" /></label><br />
 * 	<fieldset>
 * 		<label>Player Name: <input type="text" id="playername" name="playername" /> </label>
 * 	</fieldset>
 * 	<input type="button" id="addButton1" name="add" value="Add another Player" class="add-button" /><br/>
 *	<input type="submit" id="submit" name="submit" value="Submit" class="submit-button" />
 * </form>
 *
 * basic usage:
 *
 * $('#addButton1').dynamicForm();
 *
 * usage with options:
 * 
 * $('#addButton1').dynamicForm({
 * 	deleteButtonDiv: 'delete-button-div',
 * 	deleteButtonClass: 'delete-button',
 * 	deleteButtonValue: 'Delete This Fieldset',
 * 	maxFields: false,
 * 	numTimes: 1,
 * 	fadeDuration: 'slow'
 * });
 *
 */
(function($) {
	$.fn.dynamicForm = function(options) {
		var opts = $.extend( {}, $.fn.dynamicForm.defaults, options);
		return this.each(function() {
			$this = $(this);
			var o = $.meta ? $.extend( {}, opts, $this.data()) : opts;
			$(this).click(function() {
				addFieldset(o, $(this));
			});
		});
	}

	function addFieldset(options, addButtonObj) {

		var fieldsetEls = getImmediateSiblings(addButtonObj, 'FIELDSET'); //get all fieldset tags above the add button
		var fieldsetElsLen = fieldsetEls.length; //get the length of above

		if (!options.maxFields
				|| ((fieldsetElsLen + options.numTimes) <= options.maxFields)) {
			var clone = fieldsetEls[0].clone(); //clone the first fieldset
			var db = getDeleteButtonObj(options); //create its delete button
			db.click(function() { //add delete button event
						var parent = $(this).parent('fieldset');
						parent.fadeOut(options.fadeDuration, function() {
							$(this).remove();
						});
						return false;
					});
			db.appendTo(clone); //add the delete button to the clone

			clone.find(':input').each(function() { //clear the clone's fields
						//clear the inputs http://www.learningjquery.com/2007/08/clearing-form-data
						var type = this.type;
						var tag = this.tagName.toLowerCase(); // normalize case
						// it's ok to reset the value attr of text inputs, password inputs, and textareas
						if (type == 'text' || type == 'password'
								|| tag == 'textarea')
							this.value = "";
						// checkboxes and radios need to have their checked state cleared
						// but should *not* have their 'value' changed
						else if (type == 'checkbox' || type == 'radio')
							this.checked = false;
						// select elements need to have their 'selectedIndex' property set to -1
						// (this works for both single and multiple select elements)
						else if (tag == 'select')
							this.selectedIndex = -1;
					});
			//renumber the existing fieldsets starting at 1
			var count = 1;
			jQuery.each(fieldsetEls, function() {
				this.find(':input').each(function() {
					renameField(this, 'id', count); // rename the fieldset inputs' id					
						renameField(this, 'name', count); // rename the fieldset inputs' name
					});
				count++;
			});
			//renumber the clones                        
			for ( var i = count; i < (options.numTimes + count); i++) {
				var newClone = clone.clone(true);
				newClone.find(':input').each(function() {
					renameField(this, 'id', i); // rename the fieldset inputs' id					
						renameField(this, 'name', i); // rename the fieldset inputs' name
					});
				newClone.insertBefore(addButtonObj);
			}
		} else {
			alert(options.maxFieldsMsg);
		}
	}

	function getImmediateSiblings(source, targetNodeType) {

		//expecting the targets nodes to be in a row
		//immeditately beside the source (add button)
		var siblings = new Array();
		jQuery.each(source.prevAll(), function() {
			if (this.tagName == targetNodeType) {
				siblings.unshift($(this));
			} else {
				return siblings;
			}
		});
		return siblings;
	}

	function renameField(obj, attr, num) {
		var a = $(obj).attr(attr).split(/_[0-9]*$/i)[0];
		$(obj).attr(attr, a + '_' + num);
	}

	function getDeleteButtonObj(options) {
		var html = '<div class="' + options.deleteButtonDiv + '">'
				+ '<input type="button"value="' + options.deleteButtonValue
				+ '"' + ' class="' + options.deleteButtonClass + '" />'
				+ '</div>';
		return $(html);
	}

	$.fn.dynamicForm.defaults = {
		numTimes : 1,
		maxFields : false,
		maxFieldsMsg : 'You have reached the maximum number of fields allowed',
		fadeDuration : 'slow',
		deleteButtonDiv : 'delete-button-div',
		deleteButtonClass : 'delete-button',
		deleteButtonValue : 'Delete This Fieldset'
	}
})(jQuery);