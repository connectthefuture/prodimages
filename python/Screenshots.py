##### Takes 2 Images on Pasteboard from Iphone and composes both images side by side in a new file to Compare both 
###Returns a new image to iPhone attached via Pasteboard
import clipboard
import Image
import console


im1 = clipboard.get_image(idx=0)
im2 = clipboard.get_image(idx=1)
background = Image.new('RGBA', (746,650), (255, 255, 255, 255))

def main():
		console.clear()
		print "Generating image..."
		console.show_activity()

		_1 = im1.resize((366,650),Image.ANTIALIAS)
		_2 = im2.resize((366,650),Image.ANTIALIAS)
		background.paste(_1,(0,0))
		background.paste(_2,(380,0))
		background.show()
		console.hide_activity()

		clipboard.set_image(background, format='jpeg', jpeg_quality=0.80)
		print "\n\n Image set to clipboard"
	
	
console.clear()
print "Create now or Control? \n"

print "[1] Create"

print "[2] Control \n"

set_mode = raw_input("Select a mode: ")

if set_mode == "x":

    print "Exited"

elif set_mode == "1":
	
		if __name__ == '__main__':
			main()

elif set_mode == "2":

		print "\n\n"
		
		print "Which image goes on the left? (in Photos.app order) \n"

		print "[1] The first image"

		print "[2] The second image \n"
	
		set_im = raw_input("Select an image: ")

		if set_im == "x":

				print "Exited"

		else:

    			print "\n\n"

		if set_im == "1":
	
			if __name__ == '__main__':
				main()

		elif set_im == "2":
			console.clear()
			print "Generating image..."
			console.show_activity()
	
			_1 = im1.resize((366,650),Image.ANTIALIAS)
			_2 = im2.resize((366,650),Image.ANTIALIAS)

			background.paste(_1,(380,0))
			background.paste(_2,(0,0))
			background.show()
			console.hide_activity()
		
			clipboard.set_image((background), format='jpeg', jpeg_quality=0.80)
			
			print "\n\n Image set to clipboard"
