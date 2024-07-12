$("form[name=signup]").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

$("form[name=login]").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/login",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      window.location.href = "/dashboard";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});


$(document).ready(function() {

    function getGenres(resp) {
            const bluesCountObj = resp.find(item => item._id === 'blues');
            const bluesCount = bluesCountObj ? bluesCountObj.count : 0;

            const classicalCountObj = resp.find(item => item._id === 'classical');
            const classicalCount = classicalCountObj ? classicalCountObj.count : 0;

            const countryCountObj = resp.find(item => item._id === 'country');
            const countryCount = countryCountObj ? countryCountObj.count : 0;

            const discoCountObj = resp.find(item => item._id === 'disco');
            const discoCount = discoCountObj ? discoCountObj.count : 0;

            const hiphopCountObj = resp.find(item => item._id === 'hiphop');
            const hiphopCount = hiphopCountObj ? hiphopCountObj.count : 0;

            const jazzCountObj = resp.find(item => item._id === 'jazz');
            const jazzCount = jazzCountObj ? jazzCountObj.count : 0;

            const metalCountObj = resp.find(item => item._id === 'metal');
            const metalCount = metalCountObj ? metalCountObj.count : 0;

            const popCountObj = resp.find(item => item._id === 'pop');
            const popCount = popCountObj ? popCountObj.count : 0;

            const reggaeCountObj = resp.find(item => item._id === 'reggae');
            const reggaeCount = reggaeCountObj ? reggaeCountObj.count : 0;

            const rockCountObj = resp.find(item => item._id === 'rock');
            const rockCount = rockCountObj ? rockCountObj.count : 0;

            const yValues = [bluesCount, classicalCount, countryCount, discoCount, hiphopCount, jazzCount, metalCount, popCount, reggaeCount, rockCount];
            return yValues;
        }

    $.ajax({
    url: "/statistics",
    type: "GET",
    success: function(resp) {

        const xValues = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"];
        yValues = getGenres(resp);
        const colours = [
            "#D94165",
            "#EF476F",
            "#F78C6B",
            "#FFD166",
            "#83D483",
            "#06D6A0",
            "#0CB0A9",
            "#118AB2",
            "#0C637F",
            "#073B4C"
        ];
        window.statistics = new Chart("statistics", {
            type: "pie",
            data: {
                labels: xValues,
                datasets: [{
                    backgroundColor: colours,
                    data: yValues
                }],
            },
            options: {
            responsive: true,
            title: {
                display: true,
                text: "Your Music By Genre"
            },
            legend: {
                position: 'bottom',
            }
            }
        });
    },
    error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
});

    $('#recButton').click(function() {
        $('#recButton').toggleClass('notRec Rec');
        $('#recMessage').text('Recording...');
        var formData = $('form[name="record"]').serialize();
        $.ajax({
            url: '/record',
            type: 'POST',
            data: formData,
            success: function(data) {
                console.log(data);
                $('#genre').text(data.genre);
                $('#tempo').text(data.tempo);
                $('#duration').text(data.duration);
                $('#predictionResult').fadeIn();
                $('#recMessage').text('Finished recording');
                $('#recButton').toggleClass('notRec Rec');
            },
            error: function(error) {
                $error.text(resp.responseJSON.error).removeClass("error--hidden");
            }
        });

    setTimeout(function() {
        $.ajax({
        url: "/statistics",
        type: "GET",
        success: function(resp) {
            var chart = document.getElementById('statistics').getContext('2d');
            yValues = getGenres(resp);
            statistics.data.datasets[0].data = yValues;
            statistics.update();
        },
        error: function(resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
        });
    }, 20000);
        return false;
    });
});

