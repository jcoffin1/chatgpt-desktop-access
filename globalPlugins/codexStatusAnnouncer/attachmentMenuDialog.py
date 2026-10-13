"""Native list for choosing an option from ChatGPT's Add files and more popup."""

import addonHandler
import wx

from .core import attachmentOptionLabel


addonHandler.initTranslation()


class AttachmentMenuDialog(wx.Dialog):
	"""Arrow through the popup's options and press Enter to choose one."""

	def __init__(self, parent, options, onClose):
		"""``onClose`` receives the chosen option, or None when cancelled."""
		super().__init__(parent, title=_("Add files and more"))
		self._options = tuple(options)
		self._visible = self._options
		self._onClose = onClose
		self._chosen = None
		self._closing = False
		main = wx.BoxSizer(wx.VERTICAL)
		main.Add(wx.StaticText(self, label=_("&Options:")), flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
		self.optionList = wx.ListBox(self, style=wx.LB_SINGLE)
		main.Add(self.optionList, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		main.Add(wx.StaticText(self, label=_("&Filter options:")), flag=wx.LEFT | wx.RIGHT, border=10)
		self.filter = wx.TextCtrl(self)
		main.Add(self.filter, flag=wx.EXPAND | wx.ALL, border=10)
		buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		main.Add(buttons, flag=wx.EXPAND | wx.ALL, border=10)
		self.SetSizerAndFit(main)
		self.SetMinSize((560, 420))
		self.SetSize((700, 520))
		self.CentreOnScreen()
		self.filter.Bind(wx.EVT_TEXT, self._onFilter)
		self.optionList.Bind(wx.EVT_LISTBOX_DCLICK, self._onOk)
		self.Bind(wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, lambda event: self.Close(), id=wx.ID_CANCEL)
		self.Bind(wx.EVT_CHAR_HOOK, self._onCharHook)
		self.Bind(wx.EVT_CLOSE, self._onCloseEvent)
		self._showOptions()
		self.optionList.SetFocus()

	def _showOptions(self):
		self.optionList.Set([attachmentOptionLabel(option) for option in self._visible])
		if self._visible:
			self.optionList.SetSelection(0)

	def _onFilter(self, event):
		query = " ".join(self.filter.GetValue().casefold().split())
		self._visible = tuple(
			option for option in self._options
			if not query or query in attachmentOptionLabel(option).casefold()
		)
		self._showOptions()

	def _onOk(self, event):
		index = self.optionList.GetSelection()
		if not 0 <= index < len(self._visible):
			return
		self._chosen = self._visible[index]
		self.Close()

	def _onCharHook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
			return
		if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER) and self.FindFocus() is self.optionList:
			self._onOk(event)
			return
		event.Skip()

	def _onCloseEvent(self, event):
		# Destroy explicitly; wx.Dialog's default close handling would only
		# re-send Cancel to this same handler.
		if self._closing:
			return
		self._closing = True
		chosen = self._chosen
		self.Hide()
		self.Destroy()
		self._onClose(chosen)
