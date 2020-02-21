// AJAX POST
$(document).ready(function(){
  document.querySelector('#sentit').value = monitor_text
  var $myForm = $("#Gcode_form")
  $myForm.submit(function(event){
    event.preventDefault()
    var $formData = $(this).serialize()
    var $endpoint = window.location.href
    $.ajax({
      method: 'POST',
      url:    $endpoint,
      data:   $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })
  })

  function handleFormSuccess(data, textStatus, jqXHR){
      afterSentit()
      console.log(textStatus)
      $myForm[0].reset(); // reset form data
  }

  function handleFormError(jqXHR, textStatus, errorThrown){
  }
})

// Erase button
function erase(){
  event.preventDefault()
  document.getElementById("id_chattext").value = ''
}

// MONITOR CONTROLLER
function afterSentit(){
    document.getElementById('sentit').scrollTop = document.getElementById("sentit").scrollHeight
    document.getElementById('id_chattext').value = ''
    document.getElementById('id_chattext').focus();
}

// Slider
function sliderChange(val,id){
  document.getElementById(id).value = val;
}

// Buttons move
$(document).ready(function(){
  afterSentit()
  document.querySelector('#sentit').value = monitor_text
  var $myForm = $(".move-form")
  $myForm.submit(function(event){
    button_pressed = document.activeElement.id
    event.preventDefault()
    var $formData = $(this).serialize() + "&button="+button_pressed
    var $endpoint = window.location.href
    var $speedrange = document.getElementById("speedrange").value
    $.ajax({
      method: 'POST',
      url:    $endpoint,
      data:   $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })
  })
  function handleFormSuccess(data, textStatus, jqXHR){
      document.getElementById("sentit").value = data.monitor
      afterSentit()
  }

  function handleFormError(jqXHR, textStatus, errorThrown){
    afterSentit()
  }
})
