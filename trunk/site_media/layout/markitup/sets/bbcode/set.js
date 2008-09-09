// ----------------------------------------------------------------------------
// markItUp!
// ----------------------------------------------------------------------------
// Copyright (C) 2007 Jay Salvat
// http://markitup.jaysalvat.com/
// ----------------------------------------------------------------------------
myBbcodeSettings = {
  nameSpace:          "bbcode", // Useful to prevent multi-instances CSS conflict
  previewParserPath:  "/forum/bbcode/",
  markupSet: [        
      {name:'Bold', key:'B', openWith:'[b]', closeWith:'[/b]'}, 
      {name:'Italic', key:'I', openWith:'[i]', closeWith:'[/i]'}, 
      {name:'Underline', key:'U', openWith:'[u]', closeWith:'[/u]'}, 
      {separator:'---------------' },
      {name:'Picture', key:'P', replaceWith:'[img][![Url]!][/img]'}, 
      {name:'Link', key:'L', openWith:'[url=[![Url]!]]', closeWith:'[/url]', placeHolder:'Your text to link here...'},
      {separator:'---------------' },
      {name:'Quotes', openWith:'[quote]', closeWith:'[/quote]'}, 
      {name:'Code', openWith:'[code]', closeWith:'[/code]'},
      {name:'Python', openWith:'[python]', closeWith:'[/python]'}, 
      {separator:'---------------' },
      {name:'Clean', className:"clean", replaceWith:function(h) { return h.selection.replace(/\[(.*?)\]/g, "") } },
      {name:'Preview', className:"preview", call:'preview' }
   ]
}