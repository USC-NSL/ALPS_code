/*
 * Function: Store the position of ground truth object in given images
 * Input: ./img_marker [int_tag] [img_path_1] .. [img_path_n]
 * Output: Multiple files in a folder. Each file's name is for one of the images. 
          The content line is '[tag] [x] [y] [width] [height]'
          Note that x and y represents the CENTER point of the box
          All numbers are expressed in ratio to the image width/height 
 */

// 
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <stdio.h>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <fstream>
#include <cctype>

using namespace std;
using namespace cv;

#define RES_DIR "pos/" // this dir must exist together w/ the compiled program
#define MIN_SIZE 10 // if the box is smaller than this size, ignore.

Mat org; // image read in  
Mat img; // image to show
Mat tmp; // temporary image for displaying the box

static int tag; // label of the object
static string position_file; // position data will be stored here

string getFileName(string fname) {
    int startPos = fname.find_last_of("/");
    string imageName = fname.substr(startPos + 1, fname.length()); // exclude content before '/'
    return imageName.substr(0, imageName.find_last_of(".")); // exclude the '.jpg'
}

// append a line to a text file with / endl
void appendFile(string msg, string path) {
  ofstream outfile; // output file handler
  outfile.open(path, ofstream::app);
  outfile << msg << endl;
  outfile.close();
}

void on_mouse(int event,int x,int y,int flags,void *ustc) { 
  static Point pre_pt = Point(-1,-1); // initial position
  static Point cur_pt = Point(-1,-1); // mouse position

  char temp[16];
  if (event == CV_EVENT_LBUTTONDOWN) {// Press down the left key
    org.copyTo(img);
    sprintf(temp,"(%d,%d)",x,y);
    pre_pt = Point(x,y);
    putText(img,temp,pre_pt,FONT_HERSHEY_SIMPLEX,0.5,Scalar(0,0,0,255),1,8);// show the coordinate
    circle(img,pre_pt,2,Scalar(255,0,0,0),CV_FILLED,CV_AA,0);// draw the initial point that the mouse pressed
    imshow("img",img);
  }
  else if (event == CV_EVENT_MOUSEMOVE && !(flags & CV_EVENT_FLAG_LBUTTON)) {// Mouse move w/o key pressed
    img.copyTo(tmp);
    sprintf(temp,"(%d,%d)",x,y);
    cur_pt = Point(x,y);
    putText(tmp,temp,cur_pt,FONT_HERSHEY_SIMPLEX,0.5,Scalar(0,0,0,255));
    imshow("img",tmp);
  }
  else if (event == CV_EVENT_MOUSEMOVE && (flags & CV_EVENT_FLAG_LBUTTON)) { // Draw the box while moving the mouse
    img.copyTo(tmp);
    sprintf(temp,"(%d,%d)",x,y);
    int cur_x = (x >= img.cols) ? img.cols - 1 : x;
    int cur_y = (y >= img.rows) ? img.rows - 1 : y;
    cur_pt = Point(cur_x,cur_y);
    putText(tmp,temp,cur_pt,FONT_HERSHEY_SIMPLEX,0.5,Scalar(0,0,0,255));
    rectangle(tmp,pre_pt,cur_pt,Scalar(0,255,0,0),1,8,0);
    imshow("img",tmp);
  }
  else if (event == CV_EVENT_LBUTTONUP) { // show the box after depressing left key
    org.copyTo(img);
    sprintf(temp,"(%d,%d)",x,y);
    int cur_x = (x >= img.cols) ? img.cols - 1 : x;
    int cur_y = (y >= img.rows) ? img.rows - 1 : y;
    cur_pt = Point(cur_x,cur_y);
    putText(img,temp,cur_pt,FONT_HERSHEY_SIMPLEX,0.5,Scalar(0,0,0,255));
    circle(img,pre_pt,2,Scalar(255,0,0,0),CV_FILLED,CV_AA,0);
    rectangle(img,pre_pt,cur_pt,Scalar(0,255,0,0),1,8,0); 
    imshow("img",img);
    img.copyTo(tmp);
    // decide if the box is too small
    int width = abs(pre_pt.x - cur_pt.x); // get the wid/hei of cropped area
    int height = abs(pre_pt.y - cur_pt.y);
    if (width < MIN_SIZE || height < MIN_SIZE) return;
    // store a line to position file
    string line = to_string(tag) + 
              " " + to_string(((float)pre_pt.x + (float)width / 2) / (float)img.cols) +  // center point of the box
              " " + to_string(((float)pre_pt.y + (float)height / 2) / (float)img.rows) + 
              " " + to_string((float)width / (float)img.cols) + 
              " " + to_string((float)height / (float)img.rows);
    appendFile(line, position_file);
  }
}

int main(int argc, char** argv) {
  // input format: ./marker [image_path] [win_width] [win_height]
  if (argc < 3) {
    cout << "ERROR: wrong argc! Should be: ./marker [tag] [image_1] .. [image_n]" << endl;
    return -1;
  }

  tag = stoi(argv[1]);

  for (int i = 2; i < argc; i++) {
    string img_path = string(argv[i]);
    org = imread(img_path); // read in original image
    org.copyTo(img);
    org.copyTo(tmp);
    position_file = string(RES_DIR) + getFileName(img_path) + string(".txt"); // the position files
    
    ofstream outfile; // create position file for the image (Yolo requires every image w/ a pos file)
    outfile.open(position_file, ofstream::app);
    outfile.close();

    namedWindow("img"); // show the original image
    setMouseCallback("img", on_mouse, 0); // main function
    imshow("img",img);
    waitKey(0);
  }

  return 0;
}
