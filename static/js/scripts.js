
// Main script file
function prepareDocument(){
    // code to prepare our page
    jQuery("form#search").submit(function(){
        text = jQuery("#id_q").val();
        if(text == "" || text == "Search"){
            // if empty, pop up alert
            alert("Enter a search term.");
            // stop form submission
            return false;
        }
    });
}

jQuery(document).ready(prepareDocument);
