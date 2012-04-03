#where noted, code adapted from http://code.enthought.com/projects/traits/docs/html/tutorials/traits_ui_scientific_app.html
import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from enthought.traits.api import Any, Instance
from enthought.traits.ui.wx.editor import Editor
from enthought.traits.ui.wx.basic_editor_factory import BasicEditorFactory

from threading import Thread
from time import sleep
from enthought.traits.api import *
from enthought.traits.ui.api import View, Item, Group, HSplit, Handler, VSplit, VGroup, HGroup
from enthought.traits.ui.menu import NoButtons
from matplotlib.figure import Figure
from scipy import * 
from numpy import *
import wx
import urllib2, json, urllib
import Image, StringIO, ImageFilter, ImageOps


#class from http://code.enthought.com/projects/traits/docs/html/tutorials/traits_ui_scientific_app.html
#to display matplotlib figures
class _MPLFigureEditor(Editor):

	scrollable  = True

	def init(self, parent):
		self.control = self._create_canvas(parent)
		self.set_tooltip()

	def update_editor(self):
		pass

	def _create_canvas(self, parent):
		""" Create the MPL canvas. """
		# The panel lets us add additional controls.
		panel = wx.Panel(parent, -1, style=wx.CLIP_CHILDREN)
		sizer = wx.BoxSizer(wx.VERTICAL)
		panel.SetSizer(sizer)
		# matplotlib commands to create a canvas
		mpl_control = FigureCanvas(panel, -1, self.value)
		sizer.Add(mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW)
		toolbar = NavigationToolbar2Wx(mpl_control)
		sizer.Add(toolbar, 0, wx.EXPAND)
		self.value.canvas.SetMinSize((10,10))
		return panel

#class from http://code.enthought.com/projects/traits/docs/html/tutorials/traits_ui_scientific_app.html
#to display matplotlib figures
class MPLFigureEditor(BasicEditorFactory):

	klass = _MPLFigureEditor

class Query(HasTraits):
	'''object representing the query search box'''
	query_string = String('Enter a search term')
	
class ControlPanel(HasTraits):
	""" object that controls the display and contains the user interface.
	"""
	
	#the search box
	query = Instance('Query', ())
	#the url display box
	url = String('Image URL will appear here')
	#the button to run the search query
	do_search = Button('Run Query')
	#the figure
	figure = Instance(Figure)
	
	#the bottons to do the image editing
	blur = Button('Blur')
	contour = Button('Contour')
	contrast = Button('Auto Contrast')
	revert = Button('Revert')
	edge = Button('Edges')
	
	#images that are being displayed
	self.images = {}

	#configure the view for the control panel
	view = View(VGroup(
					VGroup(
						HGroup(
							Item('query', show_label=False, resizable=True ),
							Item('do_search', show_label=False),
							style='custom',
						),
						label="Input",),
					VGroup(
						
							Item('url', show_label=False, style='readonly', springy=True,),
													
					label='Image URL',),
					HGroup(
						
							Item('blur', show_label=False,),
							Item('contour', show_label=False),
							Item('contrast', show_label=False),
							Item('edge', show_label=False),
							Item('revert', show_label=False),
					orientation='horizontal'),
				), width = 1.0,
				)
				
	def _do_search_fired(self):
		'''
		method called when the search botton is clicked
		'''
		
		#url to do the search
		searchString = 'http://api.bing.net/json.aspx?Appid=F03B735C20BDC55A5D86F403273383C55D36CDBA&'+urllib.urlencode({'query':self.query.query_string})+'&sources=image'
		#load the result
		result = json.load(urllib2.urlopen(searchString))
		resultList = result['SearchResponse']['Image'] 
		
		#check to see if any results were returned
		if 'Results' in resultList > 0:
			#if so, get the first url
			foundURL = resultList['Results'][0]['MediaUrl']
		
			#attempt to open the url corresponding to the image
			try:
				#get the image
				imgopener = urllib2.build_opener()
				imgopener.addheaders = [('User-agent', 'Mozilla/5.0')]
				imgpage = imgopener.open(foundURL)
				my_picture = imgpage.read()
				
				#change the contents of the url box
				self.url = result['SearchResponse']['Image']['Results'][0]['MediaUrl']
				
				#read the picture from the returned string
				img = Image.open(StringIO.StringIO(my_picture))
				
				#save the image and display it
				self.images = {}
				self.images['current'] = img
				self.images['original'] = img.copy()
				self.image_show(img)
			except:
				self.url = 'The url could no be opened'
		else:
			self.url = 'The search did not return any results'
		
	def _blur_fired(self):
		'''
		function for when the blur button is clicked--applies ImageFilter.BLUR filter to the image
		'''
		self.addFilter(ImageFilter.BLUR)
	
	def _contour_fired(self):
		'''
		function for when the contour button is clicked--applies ImageFilter.CONTOUR filter to the image
		'''
		self.addFilter(ImageFilter.CONTOUR)
		
	def _edge_fired(self):
		'''
		function for when the edge button is clicked--applies ImageFilter.EDGE_ENCHANCE_MORE filter to the image
		'''
		self.addFilter(ImageFilter.EDGE_ENHANCE_MORE)
		
	def _contrast_fired(self):
		'''
		function for when the contrast button is clicked--applies ImageOps.autocontrast method to the image
		'''
		self.images['current'] = ImageOps.autocontrast(self.images['current'])
		self.image_show(self.images['current'])
		
	def _revert_fired(self):
		'''
		restores the image to its original state
		'''
		self.images['current'] = self.images['original'].copy()
		self.image_show(self.images['current'])
		
	def addFilter(self, fil):
		'''
		method that applies a given filter fil to an image and then displays the result
		'''
		tostr = str(fil)
		if tostr not in self.images:
			self.images['current'] = self.images['current'].filter(fil)
		self.image_show(self.images['current'])

	def image_show(self, image):
		""" 
		displays an image in the matplotlib window
		"""
		self.figure.axes[0].images=[]
		self.figure.axes[0].imshow(image, origin='lower')
		wx.CallAfter(self.figure.canvas.draw)

class MainWindowHandler(Handler):
	'''
	class to control exiting from the window
	'''
	def close(self, info, is_OK):
		return True

class MainWindow(HasTraits):
	""" 
	the main window that controls everything
	adapted from http://code.enthought.com/projects/traits/docs/html/tutorials/traits_ui_scientific_app.html
	"""
	
	#the figure
	figure = Instance(Figure)
	
	#the control panel
	panel = Instance(ControlPanel)

	def _figure_default(self):
		'''
		set the defaults for the figure
		'''
		figure = Figure()
		figure.add_axes([0.05, 0.04, 0.9, 0.92])
		figure.axes[0].get_xaxis().set_ticks([])
		figure.axes[0].get_yaxis().set_ticks([])
		return figure

	def _panel_default(self):
		'''
		set the defaults for the control panel
		'''
		return ControlPanel(figure=self.figure)
	
	#display everything
	view = View(VSplit(Item('figure', editor=MPLFigureEditor(),
							dock='vertical'),
					   Item('panel', style="custom"),
					   show_labels=False,
					  ),
				resizable=True,
				height=0.9, width=0.5,
				handler=MainWindowHandler(),
				buttons=NoButtons)

if __name__ == '__main__':
	MainWindow().configure_traits()