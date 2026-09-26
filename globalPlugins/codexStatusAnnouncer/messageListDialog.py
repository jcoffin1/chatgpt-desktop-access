"""A native, read-only list of the current conversation's visible turns."""

import addonHandler
import wx


addonHandler.initTranslation()


class MessageListDialog(wx.Dialog):
	"""Keep message review separate from ChatGPT's live document and prompt."""

	def __init__(self, parent, messages, onRefresh, onClose):
		super().__init__(parent, title=_("Conversation messages"))
		self._messages = ()
		self._visible = ()
		self._onRefresh = onRefresh
		self._onClose = onClose
		self._closing = False
		main = wx.BoxSizer(wx.VERTICAL)
		main.Add(wx.StaticText(self, label=_("Search messages:")), flag=wx.LEFT | wx.RIGHT | wx.TOP, border=10)
		self.search = wx.TextCtrl(self)
		main.Add(self.search, flag=wx.EXPAND | wx.ALL, border=10)
		main.Add(wx.StaticText(self, label=_("Messages, oldest to newest:")), flag=wx.LEFT | wx.RIGHT, border=10)
		self.messageList = wx.ListBox(self, style=wx.LB_SINGLE)
		main.Add(self.messageList, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
		main.Add(wx.StaticText(self, label=_("Selected message text:")), flag=wx.LEFT | wx.RIGHT, border=10)
		self.messageText = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
		main.Add(self.messageText, proportion=2, flag=wx.EXPAND | wx.ALL, border=10)
		self.status = wx.StaticText(self, label="")
		main.Add(self.status, flag=wx.LEFT | wx.RIGHT, border=10)
		self.refreshButton = wx.Button(self, label=_("&Refresh messages"))
		main.Add(self.refreshButton, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)
		main.Add(self.CreateButtonSizer(wx.CANCEL), flag=wx.EXPAND | wx.ALL, border=10)
		self.SetSizerAndFit(main)
		self.SetMinSize((620, 460))
		self.SetSize((760, 560))
		self.CentreOnScreen()
		self.search.Bind(wx.EVT_TEXT, self._filter)
		self.search.Bind(wx.EVT_KEY_DOWN, self._onSearchKey)
		self.messageList.Bind(wx.EVT_LISTBOX, self._selected)
		self.messageList.Bind(wx.EVT_LISTBOX_DCLICK, self._focusText)
		self.messageList.Bind(wx.EVT_KEY_DOWN, self._onListKey)
		self.refreshButton.Bind(wx.EVT_BUTTON, self._refresh)
		self.Bind(wx.EVT_BUTTON, lambda event: self.Close(), id=wx.ID_CANCEL)
		self.Bind(wx.EVT_CHAR_HOOK, self._onCharHook)
		self.Bind(wx.EVT_CLOSE, self._close)
		self.updateMessages(messages)

	def updateMessages(self, messages):
		self._messages = tuple(messages or ())
		self._filter(None)

	def _filter(self, event):
		query = self.search.GetValue().strip().casefold()
		self._visible = tuple(
			(index, speaker, text) for index, (speaker, text) in enumerate(self._messages, 1)
			if query in text.casefold() or query in speaker.casefold()
		)
		labels = []
		for index, speaker, text in self._visible:
			who = _("You") if speaker == "user" else _("ChatGPT")
			preview = text[:100] + ("…" if len(text) > 100 else "")
			labels.append(_("Message {number}, {speaker}: {preview}").format(
				number=index, speaker=who, preview=preview,
			))
		self.messageList.Set(labels)
		if labels:
			self.messageList.SetSelection(len(labels) - 1)
		self._selected(None)
		self.status.SetLabel(_("{shown} of {total} cached messages shown; older messages remain in ChatGPT's conversation view").format(
			shown=len(labels), total=len(self._messages),
		))

	def _selected(self, event):
		index = self.messageList.GetSelection()
		self.messageText.ChangeValue(self._visible[index][2] if 0 <= index < len(self._visible) else "")

	def _onSearchKey(self, event):
		if event.GetKeyCode() == wx.WXK_DOWN and self.messageList.GetCount():
			self.messageList.SetFocus()
			self.messageList.SetSelection(0)
			self._selected(None)
		else:
			event.Skip()

	def _onListKey(self, event):
		if event.GetKeyCode() in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.messageText.SetFocus()
		else:
			event.Skip()

	def _focusText(self, event):
		self.messageText.SetFocus()

	def _refresh(self, event):
		messages = self._onRefresh()
		if messages is None:
			self.status.SetLabel(_("Refreshing conversation messages…"))
			return
		self.updateMessages(messages)
		self.messageList.SetFocus()

	def _onCharHook(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
			return
		event.Skip()

	def _close(self, event):
		if not self._closing:
			self._closing = True
			self._onClose()
		event.Skip()
