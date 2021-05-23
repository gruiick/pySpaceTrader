<map version="freeplane 1.7.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="pySpaceTrader" FOLDED="false" ID="ID_1567394985" CREATED="1563971092848" MODIFIED="1564567794995" STYLE="oval" VGAP_QUANTITY="0.0 pt">
<font SIZE="14"/>
<hook NAME="MapStyle">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" show_note_icons="true" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24.0 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ICON_SIZE="12.0 pt" COLOR="#000000" STYLE="fork">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10.0 pt" SHAPE_VERTICAL_MARGIN="10.0 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="14" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Items/Goods" POSITION="right" ID="ID_413199617" CREATED="1564488896127" MODIFIED="1564572365625" LINK="#ID_1801415478" HGAP_QUANTITY="64.99999848008159 pt" VSHIFT_QUANTITY="-56.99999830126768 pt">
<edge STYLE="sharp_bezier" COLOR="#ff0000" WIDTH="1"/>
<richcontent TYPE="DETAILS">

<html>
  <head>
    
  </head>
  <body>
    <p style="margin-top: 0">
      'tp',&#160;&#160;# Tech level needed for production
    </p>
    <p style="margin-top: 0">
      'tu',&#160;&#160;# Tech level needed to use
    </p>
    <p style="margin-top: 0">
      'ttp',&#160;&#160;# Tech level which produces this item the most
    </p>
    <p style="margin-top: 0">
      'plt',&#160;&#160;# Medium price at lowest tech level
    </p>
    <p style="margin-top: 0">
      'pi',&#160;&#160;# Price increase per tech level
    </p>
    <p style="margin-top: 0">
      'var',&#160;&#160;# Max percentage above or below calculated price
    </p>
    <p style="margin-top: 0">
      'dps',&#160;&#160;# Price increases considerably when this event occurs
    </p>
    <p style="margin-top: 0">
      'cr',&#160;&#160;# When this resource is available, this item is cheap
    </p>
    <p style="margin-top: 0">
      'er',&#160;&#160;# When this resource is available, this item is expensive
    </p>
    <p style="margin-top: 0">
      'mintp',&#160;&#160;# Minimum price to buy/sell in orbit
    </p>
    <p style="margin-top: 0">
      'maxtp',&#160;&#160;# Maximum price to buy/sell in orbit
    </p>
    <p style="margin-top: 0">
      'ro'&#160;&#160;# Roundoff price for trade in orbit
    </p>
  </body>
</html>
</richcontent>
<node TEXT="BuyPrice = formule(StandardPrice)" ID="ID_1198718985" CREATED="1564488907594" MODIFIED="1564571993680" HGAP_QUANTITY="16.249999932944775 pt" VSHIFT_QUANTITY="-6.749999798834338 pt"><richcontent TYPE="DETAILS">

<html>
  <head>
    
  </head>
  <body>
    <p>
      standardprice +/- dps, cr, er
    </p>
    <p>
      +/- var
    </p>
  </body>
</html>
</richcontent>
</node>
<node TEXT="SellPrice = formule(StandardPrice)" ID="ID_1659754787" CREATED="1564488913973" MODIFIED="1564572006954" HGAP_QUANTITY="25.999999642372142 pt" VSHIFT_QUANTITY="-12.74999962002039 pt"><richcontent TYPE="DETAILS">

<html>
  <head>
    
  </head>
  <body>
    <p>
      standardprice +/- var
    </p>
  </body>
</html>
</richcontent>
</node>
<node TEXT="special = fuel_price" ID="ID_1025210960" CREATED="1564488924379" MODIFIED="1564572003508" HGAP_QUANTITY="28.24999957531692 pt" VSHIFT_QUANTITY="-27.749999172985582 pt"/>
<node TEXT="StandardPrice = formule(Planet)" ID="ID_542601894" CREATED="1564488946153" MODIFIED="1564572000804" HGAP_QUANTITY="20.74999979883433 pt" VSHIFT_QUANTITY="-55.49999834597116 pt"><richcontent TYPE="DETAILS">

<html>
  <head>
    
  </head>
  <body>
    <p>
      planet.techlevel &gt; tu
    </p>
    <p>
      plt + (planet.techlevel * pi)
    </p>
    <p>
      status increase price
    </p>
    <p>
      size minimize price
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="TODO/FIXME" POSITION="right" ID="ID_1877371907" CREATED="1564489291111" MODIFIED="1564572415273" HGAP_QUANTITY="66.49999843537813 pt" VSHIFT_QUANTITY="-114.7499965801836 pt">
<icon BUILTIN="info"/>
<edge STYLE="sharp_bezier" COLOR="#0000ff"/>
<node TEXT="Class PriceSlip ?" ID="ID_1649418088" CREATED="1564489337826" MODIFIED="1564567900142" HGAP_QUANTITY="40.24999921768906 pt" VSHIFT_QUANTITY="-39.74999881535772 pt"><richcontent TYPE="DETAILS">

<html>
  <head>
    
  </head>
  <body>
    <p>
      init trop compliqu&#233;
    </p>
    <p>
      Class m&#233;riterait peut-&#234;tre d'&#234;tre s&#233;par&#233;e en deux ?
    </p>
    <p>
      manque les fonctions d'update des prix et des stocks
    </p>
  </body>
</html>
</richcontent>
</node>
<node TEXT="gestion du Cargo" ID="ID_1010995658" CREATED="1564489623609" MODIFIED="1564567852915" HGAP_QUANTITY="45.49999906122687 pt" VSHIFT_QUANTITY="12.7499996200204 pt"><richcontent TYPE="DETAILS">

<html>
  <head>
    
  </head>
  <body>
    <p>
      -&gt; spinboxes dans SimpleTable() ? (OK)
    </p>
    <p>
      &#160;&#160;-&gt; g&#233;rer l'update(to, textvariable, state) et clear()
    </p>
    <p>
      &#160;&#160;-&gt; g&#233;rer la transmission d'info (entre cargo/pods et spinbox)
    </p>
    <p>
      &#160;&#160;&#160;&#160;&#160;* l'ajout d'un good dans un pod doit diminuer la valeur 'to' de toutes les spinbox (idem retrait)
    </p>
    <p>
      &#160;&#160;&#160;&#160;* le total de l'ensemble des spinbox ne doit pas d&#233;passer 'cargo'
    </p>
  </body>
</html>
</richcontent>
</node>
<node TEXT="gestion des achats/ventes" ID="ID_1142974461" CREATED="1564489781731" MODIFIED="1564567867378" HGAP_QUANTITY="25.24999966472388 pt" VSHIFT_QUANTITY="49.499998524785084 pt"><richcontent TYPE="DETAILS">

<html>
  <head>
    
  </head>
  <body>
    <p>
      -&gt; calcul des gains/pertes
    </p>
    <p>
      &#160;&#160;* sum(good_qty * good_price)
    </p>
    <p>
      -&gt; mise &#224; jour GUI (y compris spinboxes)
    </p>
  </body>
</html>
</richcontent>
</node>
</node>
<node TEXT="python3" POSITION="left" ID="ID_454635760" CREATED="1564567289267" MODIFIED="1564572381145" HGAP_QUANTITY="42.49999915063384 pt" VSHIFT_QUANTITY="-37.499998882412946 pt">
<edge STYLE="sharp_bezier" COLOR="#00ff00"/>
<hook NAME="AlwaysUnfoldedNode"/>
<font SIZE="12" BOLD="true"/>
<node TEXT="constants.py" ID="ID_903883233" CREATED="1563972136494" MODIFIED="1564567762419" HGAP_QUANTITY="154.99999579787266 pt" VSHIFT_QUANTITY="-25.499999240040808 pt">
<cloud COLOR="#f0f0f0" SHAPE="ARC"/>
<node TEXT="imported" ID="ID_320426341" CREATED="1563971924355" MODIFIED="1563972179767" HGAP_QUANTITY="18.499999865889528 pt" VSHIFT_QUANTITY="-23.24999930709604 pt">
<node TEXT="names" ID="ID_511604606" CREATED="1563972045391" MODIFIED="1563972047429"/>
<node TEXT="regim" ID="ID_780587920" CREATED="1563972048947" MODIFIED="1563972051682"/>
<node TEXT="resources" ID="ID_1406993737" CREATED="1563972053072" MODIFIED="1563972065038"/>
<node TEXT="techlevel" ID="ID_1959300476" CREATED="1563972066748" MODIFIED="1563972069571"/>
<node TEXT="status" ID="ID_1442254048" CREATED="1563972081174" MODIFIED="1563972083232"/>
<node TEXT="shiptypes" ID="ID_1752474037" CREATED="1563972088339" MODIFIED="1563972092615"/>
<node TEXT="mercenarynames" ID="ID_727842496" CREATED="1563972279820" MODIFIED="1563972285582"/>
<node TEXT="goods" ID="ID_1194980764" CREATED="1564051106449" MODIFIED="1564051109971"/>
</node>
<node TEXT="maxplanets" ID="ID_1189006417" CREATED="1563972163353" MODIFIED="1563972225666"/>
<node TEXT="gridmin/gridmax" ID="ID_68718303" CREATED="1563972227697" MODIFIED="1563972234879"/>
<node TEXT="xmin/maxwidth" ID="ID_1790163359" CREATED="1563972236626" MODIFIED="1564567482387"/>
<node TEXT="ymin/maxheight" ID="ID_1726662547" CREATED="1563972246841" MODIFIED="1563972254270"/>
<node TEXT="bbox limit" ID="ID_1897731208" CREATED="1563972255971" MODIFIED="1564489278740"/>
<node TEXT="maxparsec" ID="ID_817951850" CREATED="1563972261700" MODIFIED="1563972265615"/>
</node>
<node TEXT="CLI/Core" ID="ID_1872866868" CREATED="1563971435692" MODIFIED="1621796872667" HGAP_QUANTITY="91.99999767541892 pt" VSHIFT_QUANTITY="-54.749998368322885 pt">
<font SIZE="12" BOLD="true"/>
<cloud COLOR="#f0f0f0" SHAPE="ARC"/>
<node TEXT="Planet()" ID="ID_915561628" CREATED="1563971607334" MODIFIED="1563971610465">
<node TEXT="name" ID="ID_1698666223" CREATED="1563973385501" MODIFIED="1563973388124"/>
<node TEXT="position(x, y)" ID="ID_324863620" CREATED="1563973391255" MODIFIED="1563973396258"/>
<node TEXT="systemSize" ID="ID_1978427820" CREATED="1563973401235" MODIFIED="1563973408833"/>
<node TEXT="techLevel" ID="ID_189657276" CREATED="1563973410308" MODIFIED="1563973414463"/>
<node TEXT="regim" ID="ID_1211765970" CREATED="1563973417534" MODIFIED="1563973420218"/>
<node TEXT="status" ID="ID_148384997" CREATED="1563973421588" MODIFIED="1563973425238"/>
<node TEXT="civilisation (systemSize + techLevel + regime + status)" ID="ID_989184101" CREATED="1563973427564" MODIFIED="1564051640895"/>
<node TEXT="fuel_price(variable selon civ)" ID="ID_1161706560" CREATED="1563973469012" MODIFIED="1563973486726"/>
<node TEXT="homeworld(True/False)" ID="ID_414197933" CREATED="1563973490972" MODIFIED="1563973505787"/>
<node TEXT="visited(True/False)" ID="ID_1245433646" CREATED="1563973509190" MODIFIED="1563973516082"/>
<node TEXT="boundingbox(xAyA, xByB)" ID="ID_445500664" CREATED="1563973520113" MODIFIED="1564051268614"/>
</node>
<node TEXT="Captain()" ID="ID_1853080047" CREATED="1563971613175" MODIFIED="1563973591451" HGAP_QUANTITY="79.99999803304678 pt" VSHIFT_QUANTITY="6.74999979883433 pt">
<node TEXT="name" ID="ID_1894240666" CREATED="1563973315698" MODIFIED="1563973319748"/>
<node TEXT="homeworld(planete)" ID="ID_1069800715" CREATED="1563973322612" MODIFIED="1563973664837"/>
<node TEXT="location(planete)" ID="ID_1010206741" CREATED="1563973333925" MODIFIED="1563973341173"/>
<node TEXT="destination(planete)" ID="ID_195531824" CREATED="1563973343907" MODIFIED="1563973350563"/>
<node TEXT="ship(ship)" ID="ID_1178107553" CREATED="1563973357848" MODIFIED="1563973363585"/>
<node TEXT="balance" ID="ID_592601322" CREATED="1563973370330" MODIFIED="1563973374884"/>
</node>
<node TEXT="Ship()" ID="ID_12242820" CREATED="1563971619610" MODIFIED="1564572075894" HGAP_QUANTITY="55.24999877065424 pt" VSHIFT_QUANTITY="11.24999966472388 pt">
<node TEXT="model" ID="ID_1655515322" CREATED="1563973562294" MODIFIED="1563973567565"/>
<node TEXT="reservoir" ID="ID_1849198350" CREATED="1563973570866" MODIFIED="1563973573783"/>
<node TEXT="gadget" ID="ID_1732222043" CREATED="1564567688280" MODIFIED="1564567692358"/>
<node TEXT="cargo{}" ID="ID_1789465090" CREATED="1564567657633" MODIFIED="1564567699667"/>
</node>
<node TEXT="create_universe()" ID="ID_1510946867" CREATED="1563971816512" MODIFIED="1563973583894" HGAP_QUANTITY="11.000000089406964 pt" VSHIFT_QUANTITY="20.999999374151248 pt"/>
<node TEXT="collision()" ID="ID_94735112" CREATED="1563971846250" MODIFIED="1563971879246"/>
<node TEXT="save_game()" ID="ID_977202720" CREATED="1563971853049" MODIFIED="1563973626810"/>
<node TEXT="load_game()" ID="ID_878959673" CREATED="1563971858507" MODIFIED="1563973635647"/>
<node TEXT="create_planetes()" ID="ID_1142773069" CREATED="1563973643209" MODIFIED="1563973686932" HGAP_QUANTITY="18.499999865889553 pt" VSHIFT_QUANTITY="-8.999999731779106 pt"/>
<node TEXT="PriceSlip()" ID="ID_1801415478" CREATED="1564572114777" MODIFIED="1564572597160">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_413199617" STARTINCLINATION="-292;-108;" ENDINCLINATION="-209;-26;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<font SIZE="12" BOLD="true"/>
</node>
</node>
<node TEXT="Tk GUI" FOLDED="true" ID="ID_1390013067" CREATED="1563971359899" MODIFIED="1621796905456" HGAP_QUANTITY="94.2499976083637 pt" VSHIFT_QUANTITY="-62.999998122453746 pt">
<font SIZE="12" BOLD="true"/>
<cloud COLOR="#f0f0f0" SHAPE="ARC"/>
<node TEXT=".grid()" ID="ID_1519894235" CREATED="1563971489976" MODIFIED="1564567500585" HGAP_QUANTITY="15.499999955296518 pt" VSHIFT_QUANTITY="-29.249999128282095 pt"/>
<node TEXT="buttons" ID="ID_1704094292" CREATED="1563971512042" MODIFIED="1563971991523" HGAP_QUANTITY="57.49999870359901 pt" VSHIFT_QUANTITY="-35.99999892711642 pt"/>
<node ID="ID_1645167146" CREATED="1563971527024" MODIFIED="1563972779784" HGAP_QUANTITY="64.99999848008162 pt" VSHIFT_QUANTITY="15.749999530613435 pt"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b>box</b>
    </p>
  </body>
</html>
</richcontent>
<node TEXT="save" ID="ID_912520964" CREATED="1563971534557" MODIFIED="1563971537838"/>
<node TEXT="open" ID="ID_238521712" CREATED="1563971540064" MODIFIED="1563971541782"/>
<node TEXT="alert" ID="ID_1239144920" CREATED="1563971548968" MODIFIED="1564051592280">
<icon BUILTIN="messagebox_warning"/>
</node>
<node TEXT="error" ID="ID_918173833" CREATED="1563972492592" MODIFIED="1564051599800">
<icon BUILTIN="closed"/>
</node>
<node TEXT="about" ID="ID_1532383542" CREATED="1563972506615" MODIFIED="1564051605072">
<icon BUILTIN="info"/>
</node>
</node>
<node ID="ID_1247509884" CREATED="1563971570193" MODIFIED="1564567610230" HGAP_QUANTITY="37.999999284744284 pt" VSHIFT_QUANTITY="54.7499983683229 pt"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p style="text-align: center">
      <font size="3"><b>notebook (onglets)</b></font>
    </p>
  </body>
</html>
</richcontent>
<font BOLD="false"/>
<node TEXT="map" ID="ID_1434916473" CREATED="1563971643743" MODIFIED="1564489087030" HGAP_QUANTITY="21.499999776482586 pt" VSHIFT_QUANTITY="-11.24999966472388 pt"/>
<node TEXT="trading" ID="ID_304981833" CREATED="1564489074227" MODIFIED="1564567643379" HGAP_QUANTITY="25.249999664723884 pt" VSHIFT_QUANTITY="14.249999575316918 pt"/>
</node>
<node FOLDED="true" ID="ID_485383990" CREATED="1563972522978" MODIFIED="1563972538072" HGAP_QUANTITY="13.250000022351742 pt" VSHIFT_QUANTITY="44.24999868124728 pt"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b>functions</b>
    </p>
  </body>
</html>
</richcontent>
<node TEXT="draw_map()" ID="ID_292217805" CREATED="1563972591352" MODIFIED="1564489218540"/>
<node TEXT="draw_gui()" ID="ID_619846372" CREATED="1564489219198" MODIFIED="1564489223854"/>
<node TEXT="get_distance()" ID="ID_134254375" CREATED="1563972601030" MODIFIED="1563972608162"/>
<node TEXT="new_game()" ID="ID_396593639" CREATED="1563972615978" MODIFIED="1563972623683"/>
<node TEXT="next_turn" ID="ID_1104371866" CREATED="1563972634586" MODIFIED="1563972641312"/>
<node TEXT="on_click()" ID="ID_1075441640" CREATED="1563972659864" MODIFIED="1563972664702"/>
<node TEXT="draw_limit()" ID="ID_745024205" CREATED="1563972670601" MODIFIED="1563972693464"/>
<node TEXT="draw_target()" ID="ID_962371549" CREATED="1563972681442" MODIFIED="1563972687667"/>
<node TEXT="refuel()" ID="ID_1795655864" CREATED="1563972701303" MODIFIED="1563972835941"/>
<node TEXT="set_destination()" ID="ID_887099038" CREATED="1563972710079" MODIFIED="1563972743926"/>
<node TEXT="show_homeworld()" ID="ID_294458101" CREATED="1563972729834" MODIFIED="1563972748657"/>
<node TEXT="show_location()" ID="ID_928877739" CREATED="1563972754369" MODIFIED="1563972759246"/>
<node TEXT="update_affiche()" ID="ID_307024468" CREATED="1563972762182" MODIFIED="1563972768303"/>
</node>
<node TEXT="SimpleTable()" ID="ID_1240382725" CREATED="1564489377660" MODIFIED="1564489385374" VSHIFT_QUANTITY="15.749999530613437 pt">
<node TEXT="clear()" ID="ID_1778731514" CREATED="1564489403866" MODIFIED="1564489406942"/>
<node TEXT="set()" ID="ID_1678644398" CREATED="1564489409131" MODIFIED="1564489413434"/>
<node TEXT=".size" ID="ID_1666635733" CREATED="1564489418749" MODIFIED="1564489428703"/>
</node>
</node>
<node TEXT="PySimpleGUI" ID="ID_1708242855" CREATED="1621796927129" MODIFIED="1621796963129">
<font SIZE="12" BOLD="true"/>
<node ID="ID_31095265" CREATED="1563972522978" MODIFIED="1563972538072" HGAP_QUANTITY="13.250000022351742 pt" VSHIFT_QUANTITY="44.24999868124728 pt"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b>functions</b>
    </p>
  </body>
</html>
</richcontent>
<node TEXT="draw_map()" ID="ID_479164759" CREATED="1563972591352" MODIFIED="1564489218540"/>
<node TEXT="draw_gui()" ID="ID_1959372616" CREATED="1564489219198" MODIFIED="1564489223854"/>
<node TEXT="get_distance()" ID="ID_995810161" CREATED="1563972601030" MODIFIED="1563972608162"/>
<node TEXT="new_game()" ID="ID_274125975" CREATED="1563972615978" MODIFIED="1563972623683"/>
<node TEXT="next_turn" ID="ID_1465498755" CREATED="1563972634586" MODIFIED="1563972641312"/>
<node TEXT="on_click()" ID="ID_1899905390" CREATED="1563972659864" MODIFIED="1563972664702"/>
<node TEXT="draw_limit()" ID="ID_237970471" CREATED="1563972670601" MODIFIED="1563972693464"/>
<node TEXT="draw_target()" ID="ID_1640185873" CREATED="1563972681442" MODIFIED="1563972687667"/>
<node TEXT="refuel()" ID="ID_1951921999" CREATED="1563972701303" MODIFIED="1563972835941"/>
<node TEXT="set_destination()" ID="ID_732072494" CREATED="1563972710079" MODIFIED="1563972743926"/>
<node TEXT="show_homeworld()" ID="ID_664563087" CREATED="1563972729834" MODIFIED="1563972748657"/>
<node TEXT="show_location()" ID="ID_1784479491" CREATED="1563972754369" MODIFIED="1563972759246"/>
<node TEXT="update_affiche()" ID="ID_1863037807" CREATED="1563972762182" MODIFIED="1563972768303"/>
</node>
<node TEXT="UI" ID="ID_187607111" CREATED="1621796995248" MODIFIED="1621797009041">
<font BOLD="true"/>
</node>
</node>
</node>
</node>
</map>
