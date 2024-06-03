document.getElementById('chart-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const time_s = document.getElementById('time-s').value;
    const samples_s = document.getElementById('samples-s').value;
    reload_chart(time_s, samples_s);
});

function reload_chart(time_s, samples_s){
    fetch(`/sensors/chart-data?sensor=1&time=${time_s}&samples=${samples_s}`)
    .then(response => response.json())
    .then(data => {
        Highcharts.chart('s1-chart', {
            chart: {
                type: 'spline',
                zoomType: 'xy',
                resetZoomButton: {
                    theme: {
                        fill: 'transparent'
                    }
                },
                backgroundColor: null,
                events: {
                    fullscreenOpen: function () {
                        this.update({
                            chart: {
                                backgroundColor: '#ffffff'
                            },
                            plotOptions: {
                                series: {
                                    marker: {
                                        radius: 3,
                                    },
                                    lineWidth: 2
                                }
                            }
                        });
                    },
                    fullscreenClose: function () {
                        this.update({
                            chart: {
                                backgroundColor: 'rgba(255, 255, 255, 0)'
                            },
                            plotOptions: {
                                series: {
                                    marker: {
                                        radius: 1,
                                    },
                                    lineWidth: 1.5
                                }
                            }
                        });
                    }
                }
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: data.categories,
                title: {
                     text: 'Date'
                }
            },
            yAxis: {
                title: {
                    text: 'ºC - %'
                }
            },
            tooltip: {
                 shared: true,
                crosshairs: true
            },
            plotOptions: {
                series: {
                    marker: {
                        enabled: true,
                         radius: 1,
                        symbol: 'circle'
                    },
                    lineWidth: 1.5
                }
            },
            legend: {
                layout: 'horizontal',
                backgroundColor: null,
            },
            navigation: {
                    buttonOptions: {
                        theme: {
                            fill: 'transparent'
                        }
                    }
            },
            exporting: {
                buttons: {
                    contextButton: {
                        theme: {
                            fill: 'transparent'
                        }
                    }
                }
            },
            series: data.series
        });
    });
  }

$(document).ready(function() {
  const time_s = document.getElementById('time-s').value;
  const samples_s = document.getElementById('samples-s').value;

  reload_chart(time_s, samples_s);
});
