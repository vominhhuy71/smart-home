using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.Net.Http;
using System.Net.Http.Headers;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;


namespace SmartHomeApplication
{
    public partial class MainWindow : Window
    {
    
        public MainWindow()
        {
            InitializeComponent();
            
        }
        private async void TextBox_TextChanged1(object sender, TextChangedEventArgs e)
        {
            while (true)
            {
                //Indoor temperature
                HttpClient client = new HttpClient();
                HttpResponseMessage response = await client.GetAsync("http://localhost:5000/info/thermistor");      
                string responseBody = await response.Content.ReadAsStringAsync();
                Thermistor Temperature = JsonConvert.DeserializeObject<Thermistor>(responseBody);
                string output = Temperature.value.ToString() + "°C";
                InTemp.Text = output;

                await Task.Delay(3000);
            }
        }

        private async void TextBox_TextChanged2(object sender, TextChangedEventArgs e)
        {
            //Outside temperature
            while (true)
            {
                HttpClient client = new HttpClient();
                HttpResponseMessage response = await client.GetAsync("http://api.openweathermap.org/data/2.5/weather?q=Mikkeli&units=metric&appid={yourid}");
                response.EnsureSuccessStatusCode();
                string responseString = await response.Content.ReadAsStringAsync();
                JObject responseBody = JObject.Parse(responseString);
                string output = responseBody.SelectToken("main.temp").ToString() + "°C ," + responseBody.SelectToken("weather[0].main").ToString();
                OutTemp.Text = output;
                await Task.Delay(10000);
            }
        }

        private void TextBox_DateTime(object sender, TextChangedEventArgs e)
        {
            Date_Time.Text = DateTime.Now.ToString("dd/MM/yyyy\nHH:MM:ss");
        }

        private bool button1WasClick = false;
        private void Button1_Click(object sender, RoutedEventArgs e)
        {

            button1WasClick = true;
            MessageBox.Show("Welcome home!");
        }

        private async void TextBox3_TextChanged(object sender, TextChangedEventArgs e)
        {          
            while (true)
            {
                HttpClient client = new HttpClient();
                HttpResponseMessage response = await client.GetAsync("http://localhost:5000/info/security");
                response.EnsureSuccessStatusCode();
                string responseString = await response.Content.ReadAsStringAsync();
                List<Item> items = JsonConvert.DeserializeObject<List<Item>>(responseString);
                var haveKey = true;
                var haveMotion = false;
                for (int i=0; i< items.Count(); i++)
                {
                    if (items[i].name == "haveMotion")
                    {
                        if (items[i].value == true)
                        {
                            haveMotion = true;
                        }
                    }
                    else if (items[i].name == "haveKey")
                    {
                        if (items[i].value == false)
                        {
                            haveKey = false;
                        }
                    }
                }

                if ((haveKey==false) && (haveMotion == true))
                {
                    Security.Text = "Motion detected! Is that you?";
                    button1.Visibility = Visibility.Visible;
                    button2.Visibility = Visibility.Visible;
                    if (button1WasClick)
                    {
                        HttpClient Temp_client = new HttpClient();
                        var responsePut = Temp_client.PutAsync("http://localhost:5000/info/security/haveKey", null).Result;
                        //Back to waiting
                        var responsePut2 = Temp_client.PutAsync("http://localhost:5000/info/security/haveMotion", null).Result;
                        button1WasClick = false;
                        haveKey = true;
                        haveMotion = false;
                    }
                }
                else
                {
                    Security.Text = "No violation!";
                    button1.Visibility = Visibility.Hidden;
                    button2.Visibility = Visibility.Hidden;
                }
                if (haveKey == true)
                {
                    button3.Visibility = Visibility.Visible;
                }
                else
                {
                    button3.Visibility = Visibility.Hidden;
                }
                await Task.Delay(1000);
            }
        }

        private void Button2_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Please call police!");
        }

        private bool bl_toggle = false;
        private void Button_Click_bL(object sender, RoutedEventArgs e)
        {
            bl_toggle = true;
        }

        private async void TextBox_TextChangedBedLight(object sender, TextChangedEventArgs e)
        {
            while (true)
            {
                HttpClient client = new HttpClient();
                HttpResponseMessage response = await client.GetAsync("http://localhost:5000/info/lights");
                string responseBody = await response.Content.ReadAsStringAsync();
                List<Lights> lights = JsonConvert.DeserializeObject<List<Lights>>(responseBody);
                string output = "off";
                for (int i = 0; i < lights.Count(); i++)
                {
                    if (lights[i].name=="bedLight")
                    {
                        if(lights[i].value == true)
                        {
                            output = "on";
                        }
                    }
                }
                bedLight.Text = output;

                if(bl_toggle)
                {
                    HttpClient Temp_client = new HttpClient();
                    var responsePut = Temp_client.PutAsync("http://localhost:5000/info/lights/bedLight", null).Result;
                    bl_toggle = false;
                }

                await Task.Delay(3000);
            }
        }
        private bool lvr_toggle = false;
        private void Button_Click_lvR(object sender, RoutedEventArgs e)
        {
            lvr_toggle = true;
        }

        private async void TextBox_TextChangedLvLight(object sender, TextChangedEventArgs e)
        {
            while (true)
            {
                HttpClient client = new HttpClient();
                HttpResponseMessage response = await client.GetAsync("http://localhost:5000/info/lights");
                string responseBody = await response.Content.ReadAsStringAsync();
                List<Lights> lights = JsonConvert.DeserializeObject<List<Lights>>(responseBody);
                string output = "off";
                for (int i = 0; i < lights.Count(); i++)
                {
                    if (lights[i].name == "lvLight")
                    {
                        if (lights[i].value == true)
                        {
                            output = "on";
                        }
                    }
                }
                lvLight.Text = output;

                if (lvr_toggle)
                {
                    HttpClient Temp_client = new HttpClient();
                    var responsePut = Temp_client.PutAsync("http://localhost:5000/info/lights/lvLight", null).Result;
                    lvr_toggle = false;
                }

                await Task.Delay(3000);
            }
        }

        private async void Button_Click_Lock(object sender, RoutedEventArgs e)
        {
            HttpClient client = new HttpClient();
            HttpResponseMessage response = await client.GetAsync("http://localhost:5000/info/security");
            response.EnsureSuccessStatusCode();
            string responseString = await response.Content.ReadAsStringAsync();
            List<Item> items = JsonConvert.DeserializeObject<List<Item>>(responseString);
            var haveKey = true;
            for (int i = 0; i < items.Count(); i++)
            {
                if (items[i].name == "haveKey")
                {
                    if (items[i].value == false)
                    {
                        haveKey = false;
                    }
                }
            }

            var responsePut = client.PutAsync("http://localhost:5000/info/security/haveKey", null).Result;
            var responsePut2 = client.PutAsync("http://localhost:5000/info/security/haveMotion", null).Result;
        }
    }
}
