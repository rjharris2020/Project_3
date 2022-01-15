function init() {
    // Grab a reference to the dropdown select element
    let selector = d3.select("#selYear");

  
    // Use the list of sample names to populate the select options
    d3.json("/api/top5ev").then((data) => {
      let year = [];
        for (let i = 0; i<Object.keys(data).length; i++) {
            let access = data[i]
           if (!year.includes(access['Year'])){
            year.push(access['Year'])
           };
        };
  
      year.forEach((obj) => {
        selector
          .append("option")
          .text(obj)
          .property("value", obj);
      });
  
      // Use the first sample from the list to build the initial plots
      let firstyear = year[0];
      buildDynamicChart(firstyear);
      buildIndicator(firstyear);
    //   buildMetadata(firstSample);
    });
    
    buildStaticChart();
  }


function optionChanged(selection) {
    // Fetch new data each time a new year is selected
    buildDynamicChart(selection);
    buildIndicator(selection)
    
  }
  


function buildStaticChart() {
    d3.json ('/api/transposed').then(function(obj) {
        let trans_data = obj;
        console.log(trans_data)
        carRegistrations = [];
        passengerEmissions = [];
        transYear=[];

        for (let i = 2000; i<2020; i++) {
            let access = trans_data[i]
            passengerEmissions.push(access["Passenger Vehicles"])
            carRegistrations.push(access["Car Registrations"])
            transYear.push(i)
        };
        
        var passengerVehicleTrace = {
            x: transYear,
            y: passengerEmissions,
            name: 'Passenger Vehicle Emissions',
            type: "line",
            line: {
                color: 'rgb(255,10,40',
                width: 2
            }
        };

        var registrationsTrace = {
            x: transYear,
            y: carRegistrations,
            name: 'Electric Vehicle Registrations',
            yaxis: 'y2',
            type: "bar",
            marker: {
                color: 'rgb(158,202,225',
                opacity: 0.5
            }
        };

        var graphData = [ registrationsTrace , passengerVehicleTrace];

        var layout = {
            // title: 'Vehicle regstrations and Passenger Vehicle emissions',
            plot_bgcolor: '#ededed',
            paper_bgcolor: '#ededed',
            yaxis: {title: 'Passenger Vehicle Emisson (MMT CO2e)'},
            yaxis2: {
              title: 'Electric Vehicle Registrations',
              titlefont: {color: 'rgb(148, 103, 189)'},
              tickfont: {color: 'rgb(148, 103, 189)'},
              overlaying: 'y',
              side: 'right'
            },
            legend: {
                x: 0,
                y: -1,
                traceorder: 'normal',
                font: {
                  family: 'sans-serif',
                  size: 12,
                  color: '#000'
                },
                bgcolor: '#ededed',
                bordercolor: '#ededed',
                borderwidth: 2
              }
        };
        Plotly.newPlot('staticChart', graphData, layout, responsive = true)
    });
};


function buildDynamicChart(year) {
    d3.json ('/api/top5ev').then(function(obj) {
        var ev = obj;
        // console.log(ev);


        var carList = [];
        for (let i = 0; i<Object.keys(ev).length; i++) {
            let placement = ev[i]
            if (placement['Year'] == year) 
                carList.push(placement)
        };
        // console.log(carList);

        var modelTrace = {
            x: carList.map(row => row['Vehicle Name']),
            y: carList.map(row => row['Carbon Emission']),
            type: "bar",
            marker: {color: '#a9a9a9',opacity: 0.9},
            line: {color: '#FF0000', width: 6}
        };
        var layout = {
            title: 'Top 5 EV and Average Yearly Emissions',
            plot_bgcolor: '#ededed',
            paper_bgcolor: '#ededed',
            yaxis: {title: 'lbs of CO2'},
        }

        let data = [modelTrace];
        Plotly.newPlot('top5ev', data, layout)





    });
};

function buildIndicator(year) {
    d3.json ('/api/energy').then(function(obj) {
        var grid = obj[2];
        
        function mean(arr) {
            let total = 0;
            for (let i = 0; i < arr.length; i++) {
              if (!isNaN(arr[i]))
                total += arr[i];
            }
            let meanValue = total / arr.length;
          
            return meanValue;
          };

        function getStandardDeviation (array) {
        const n = array.length
        const mean = array.reduce((a, b) => a + b) / n
        return Math.sqrt(array.map(x => Math.pow(x - mean, 2)).reduce((a, b) => a + b) / n)
        }
        var dif = Math.round(mean(Object.values(grid)));
        var stdDev = Math.round(getStandardDeviation(Object.values(grid).slice(11,20)));
        

        var gridEmissions = [{
            // title: { text: "Total Emissions vs average"},
            type: "indicator",
            mode: "gauge+number+delta",
            value: grid[`${year}.0`],
            number: {suffix: "MMT CO2e"},
            delta: {reference: dif, increasing: {color: "red"}, decreasing: {color: "green"}},
            gauge: {
                axis: {range: [0,150],
                    tickmode: "array",
                    tickvals: [dif-2*stdDev, dif-stdDev, dif, dif+stdDev, dif+2*stdDev],
                    ticktext: ['-2STDV','-STDV','AVG','+STDV','+2STDV']},
                bar: { color: "#10425c"},
                steps: [
                    {range: [0, dif-stdDev], color: "green" },
                    {range: [dif-stdDev, dif+stdDev], color: "yellow" },
                    {range: [dif+stdDev, 150], color: "red" }
                ],
                threshold: {
                    line: { color: "red", width: 4 },
                    thickness: 0.75,
                    value: 140
                }
            },
            domain: { row:0, column:0}
            
        }];
        var layout = {
            autosize: true,
            margin: { t: 25, r: 25, l: 25, b: 25 },
            margin: {t: 0, b: 0 },
            paper_bgcolor: '#ededed'
            
        }

        Plotly.newPlot('gauge', gridEmissions, layout)





    });
};
// Initialize the dashboard
init();