// FUNCTION: Get a standard product image and resize according to request parameters //
// test mrl: http://192.168.20.62:9090/mgen/Bluefly/prodImage.ms?productCode=0091566&width=157&height=188
function main() {
   // Create media object
   var image = new Media();
   var background = new Media();
   var virtualDirectory;
   var imageExt;
   var dashLine = new Media(); // 157x2

   // Request object variable
   var productCode = req.getParameter("productCode");
   var width = req.getParameter("width");
   var ispg = req.getParameter("ispg");
   
   var height = req.getParameter("height");
   var bgColor = req.getParameter("bgColor");

   // Determine the virtual directory by checking the size
   // of the requested image.
   if (bgColor != null) {
      virtualDirectory = "pictImages";
      imageExt = ".pct";
   }
   else {
      if (width < 200) {
         virtualDirectory = "mediumImages";
         imageExt = "_m.jpg";
      }
      else if (width >= 200) {
         virtualDirectory = "largeImages";
         imageExt = "_l.jpg";
      }
      else {
         virtualDirectory = "largeImages";
         imageExt = "_l.jpg";
      }
   }

   // Determine the hash folder from which to load the image
   // based upon the style number
   var hashFolder = productCode.charAt(6);
   if (ispg != null && ispg == "true") {
      hashFolder = productCode.charAt(9);
   }
   
   // Create image loading string from variables
   var imageString;
   // Check for gift certificates
   if (productCode.substr(0,8) == "giftcert") {
      imageString = virtualDirectory + ":/giftcerts/" + productCode + imageExt;
   }
   else {
      imageString = virtualDirectory + ":/" + hashFolder + "/" + productCode + imageExt;
   }
   print(imageString + "\n");

   // Load image into the media object from the specified file
   image.load(name @ imageString);
   var origWidth = image.getWidth();        // original size of the product image
   var origHeight = image.getHeight();
   var aspectRatio = 400 / 480;         // original aspect ratio of the product image

   var newAspectRatio;
   var fullX = origWidth;                             
                                                // size of product image at 100% magnification
   var fullY = origHeight;

   // force the original image at 100% resolution into the correct aspect 
    // ratio by padding the 'shorter' side
   if (origWidth > origHeight) {
      fullY = origWidth * (height / width);
   }
   else {
      fullX = origHeight * (width / height);
   }
   newAspectRatio = fullX / fullY;

   // Scale the image to the specified size
   if (bgColor == null) {
      bgFillColor = "0xFFFFFF";
   }
   else {
      bgFillColor = "0x" + bgColor;
   }

   background.makeCanvas(xs @ width, ys @ height, fillColor @ bgFillColor);
   if (image.getWidth() > image.getHeight()) {
      image.scale(alg @ "smooth", xs @ width, constrain @ true);
   }
   else {
      image.scale(alg @ "smooth", ys @ height, constrain @ true);
   }
   background.composite(source @ image);

   
   if (width == 157 || width == 127) {
      var yPos = 188;
      var lineImageString = "miscImages:/listphoto_line.gif";
      if (width == 127) {
         yPos = 104;
         lineImageString = "miscImages:/feat_item_photo_rule.gif";
      }
      // make dashed line image canvas
      dashLine.load(name @ lineImageString);
      background.composite(source @ dashLine, y @ yPos);
   }
   // Save media object to a specified file type
   background.save(type @ "jpeg");
}
