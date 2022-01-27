using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Drawing;
using System.Drawing.Imaging;

namespace bitmap_cache
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();

            String flag = "nc3{det_der_er_bare_så_rigtigt!}";

            {
                int width = 32 * flag.Length;
                int height = 32 + 32;
                Bitmap bmp = new Bitmap(width, height);
                using (Graphics graph = Graphics.FromImage(bmp))
                {
                    Rectangle ImageSize = new Rectangle(0, 0, width, height);
                    graph.FillRectangle(Brushes.White, ImageSize);
                    graph.DrawString(flag, new Font("Courier New", 32), Brushes.Black, 0, 0);
                }
                bmp.Save("hello.bmp");
            }


            var rand = new Random();

            for (int i = 0; i < flag.Length; i++)
            {
                int width = 32;
                int height = 32 + 32;
                Bitmap bmp = new Bitmap(width, height);
                using (Graphics graph = Graphics.FromImage(bmp))
                {
                    Rectangle ImageSize = new Rectangle(0, 0, width, height);
                    graph.FillRectangle(new SolidBrush(Color.FromArgb(255 - i, 255 - i, 255 - i)), ImageSize);
                    graph.DrawString( (flag[i]).ToString() , new Font("Courier New", 32), Brushes.Black, 0, 0);
                }

                bmp.Save("tilfældig_cachet_bitmap_" + rand.Next(1, 0xFFFFFFF) + ".bmp");
            }
        }
    }
}
 
