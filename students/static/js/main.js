function initJournal() {
  var indicator = $('#ajax-progress-indicator');
  $('.day-box input[type="checkbox"]').click(function(event){
    var box = $(this);
    $.ajax(box.data('url'), {
      'type': 'POST',
      'async': true,
      'dataType': 'json',
      'data': {
        'pk': box.data('student-id'),
        'date': box.data('date'),
        'present': box.is(':checked') ? '1': '',
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      'beforeSend': function(xhr, settings){
        indicator.show();
      },
      'error': function(xhr, status, error){
        alert(error);
        indicator.hide();
      },
      'success': function(data, status, xhr){
        indicator.hide();
      }
    });
  });
}


function initGroupSelector() {
  // look up select element with groups and attach our even handler
  // on field "change" event
  $('#group-selector select').change(function(event){
    // get value of currently selected group option
    var group = $(this).val();
    if (group) {
      // set cookie with expiration date 1 year since now;
      // cookie creation function takes period in days
      $.cookie('current_group', group, {'path': '/', 'expires': 365});
    } else {
      // otherwise we delete the cookie
      $.removeCookie('current_group', {'path': '/'});
    }
    // and reload a page
    location.reload(true);
    return true;
  });
}


function initDateFields() {
  $('input.dateinput').datetimepicker({
    'format': 'YYYY-MM-DD'
  }).on('dp.hide', function(event){
    $(this).blur();
  });
}


function initEditStudentPage() {
  $('a.student-edit-form-link, #student-add-form-link').click(function(event){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        // check if we got successfull response from the server
        if (status != 'success') {
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          return false;
        }
        // update modal window with arrived content from the server
        var modal = $('#myModal'),
            html = $(data),
            form = html.find('#content-column form');
        modal.find('.modal-title').html(html.find('#content-column h2').text());
        modal.find('.modal-body').html(form);
        // init our edit form
        initEditStudentForm(form, modal);
        // setup and show modal window finally
        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please, try again a bit later.'));
        return false;
      }
      });
    return false;
    });
}

function initEditStudentForm(form, modal) {
  // attach datepicker
  initDateFields();
  // close modal window on Cancel button click
    form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
  });
  // make form work in AJAX mode
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please, try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr) {
      var html = $(data), newform = html.find('#status_message');
      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));
      // copy form to modal if we found it in server response
      //if (newform.length > 0) {
      //  modal.find('.modal-body').append(newform);
        // initialize form fields and buttons
      //  initEditStudentForm(newform, modal);
      //} else {
        // if no form, it means success and we need to reload page
        // to get updated students list;
        // reload after 2 seconds, so that user can read
        // success message
        setTimeout(function(){location.reload(true);}, 500);
      //}
    }
  });
}

// ------- edit group modal window --------
function initEditGroupPage() {
  $('a.group-edit-form-link, #group-add-form-link').click(function(event){
    var link = $(this);
    $.ajax({
      'url': link.attr('href'),
      'dataType': 'html',
      'type': 'get',
      'success': function(data, status, xhr){
        // check if we got successfull response from the server
        if (status != 'success') {
          alert(gettext('There was an error on the server. Please, try again a bit later.'));
          return false;
        }
        // update modal window with arrived content from the server
        var modal = $('#myModal'),
            html = $(data),
            form = html.find('#content-column form');
        modal.find('.modal-title').html(html.find('#content-column h2').text());
        modal.find('.modal-body').html(form);
        // init our edit form
        initEditGroupForm(form, modal);
        // setup and show modal window finally
        modal.modal({
          'keyboard': false,
          'backdrop': false,
          'show': true
        });
      },
      'error': function(){
        alert(gettext('There was an error on the server. Please, try again a bit later.'));
        return false;
      }
      });
    return false;
    });
}

function initEditGroupForm(form, modal) {
  // attach datepicker
  initDateFields();
  // close modal window on Cancel button click
    form.find('input[name="cancel_button"]').click(function(event){
    modal.modal('hide');
    return false;
  });
  // make form work in AJAX mode
  form.ajaxForm({
    'dataType': 'html',
    'error': function(){
      alert(gettext('There was an error on the server. Please, try again a bit later.'));
      return false;
    },
    'success': function(data, status, xhr) {
      var html = $(data), newform = html.find('#content-column form');
      // copy alert to modal window
      modal.find('.modal-body').html(html.find('.alert'));
      // copy form to modal if we found it in server response
      if (newform.length > 0) {
        modal.find('.modal-body').append(newform);
        // initialize form fields and buttons
        initEditGroupForm(newform, modal);
      } else {
        // if no form, it means success and we need to reload page
        // to get updated groups list;
        // reload after 2 seconds, so that user can read
        // success message
        setTimeout(function(){location.reload(true);}, 500);
      }
    }
  });
}
// ------ end group edit modal window -----------

// ------ image avatar in to modal window -------
function initImgZoom() {
  $('.img-circle').click(function(event){
    var link = $(this);
        var modal = $('#myModal');
        modal.find('.modal-body').html("<img src='"+link.attr('src')+"'width='565'>");
        modal.modal({
          'keyboard': true,
          'backdrop': true,
          'show': true
        });
    return false;
    });
}
// ------ end image avatar in to modal window -------



$(document).ready(function(){
  initJournal();
  initGroupSelector();
  initDateFields();
  initEditStudentPage();
  initEditGroupPage();
  initImgZoom();
});