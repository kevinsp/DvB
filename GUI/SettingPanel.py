import viz
import viztracker
import vizinput
import vizshape
import vizcam
import vizmenu
import vizinfo
import viztask
import vizpopup
import vizact
import viznet
import vizdlg

import GlobalVariables

def oeffneSettingPanel(menubar):

	if (GlobalVariables.windowOpen is False):
		GlobalVariables.windowOpen = True
		menubar.setVisible(viz.OFF)
		
		blackTheme = viz.getTheme()
		blackTheme.borderColor = (0.1,0.1,0.1,1)
		blackTheme.backColor = (0.4,0.4,0.4,1)
		blackTheme.lightBackColor = (0.6,0.6,0.6,1)
		blackTheme.darkBackColor = (0.2,0.2,0.2,1)
		blackTheme.highBackColor = (0.2,0.2,0.2,1)


		myPanel = vizdlg.Panel()

		#Add row of checkboxes
		row = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		row.addItem(viz.addText('Einstellung 1'))
		check1 = row.addItem(viz.addCheckbox())
		check1.set(GlobalVariables.variable1)
		
		row.addItem(viz.addText('Einstellung 2'))
		check2 = row.addItem(viz.addCheckbox())
		check2.set(GlobalVariables.variable2)


		row2 = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		row2.addItem(viz.addText('Einstellung 3'))
		check3 = row2.addItem(viz.addCheckbox())
		check3.set(GlobalVariables.variable3)

		row2.addItem(viz.addText('Einstellung 4'))
		check4 = row2.addItem(viz.addCheckbox())
		check4.set(GlobalVariables.variable4)


		row3 = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		row3.addItem(viz.addText('Einstellung 5'))
		check5 = row3.addItem(viz.addCheckbox())
		check5.set(GlobalVariables.variable5)

		row3.addItem(viz.addText('Einstellung 6'))
		check6 = row3.addItem(viz.addCheckbox())
		check6.set(GlobalVariables.variable6)


		bestaetigePanel = vizdlg.Panel(layout=vizdlg.LAYOUT_HORZ_BOTTOM,border=False,background=False,margin=0)
		okButton = bestaetigePanel.addItem(viz.addButtonLabel("OK"))


		#Add row to myPanel
		myPanel.addItem(row)
		myPanel.addItem(row2)
		myPanel.addItem(row3)
		myPanel.addItem(bestaetigePanel)


		tp = vizdlg.TabPanel(theme=blackTheme,align=vizdlg.ALIGN_CENTER)
		tp.addPanel('Einstellungen',myPanel)

		viz.link(viz.CenterCenter,tp)

		tp.background.alpha(0.8)


		def fensterSchliessen():
			GlobalVariables.variable1 = check1.get()
			GlobalVariables.variable2 = check2.get()
			GlobalVariables.variable3 = check3.get()
			GlobalVariables.variable4 = check4.get()
			GlobalVariables.variable5 = check5.get()
			GlobalVariables.variable6 = check6.get()

			GlobalVariables.windowOpen = False
			tp.remove()

		vizact.onbuttondown(okButton,fensterSchliessen)
				
	else:
		pass
