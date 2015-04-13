This is the python package containing the Pick Pack application. The application requires Twisted and Nevow. When run with the pickpack_dev.tac file, it serves a single-page web application on port 8082.

#### Install

    cd  personal/career/portfolio/consulting/
    pip install -e common
    pip install -e pickpack/App
    cd pickpack/App/CML_Pickpack

#### Run

    twistd --nodaemon --python pickpack_dev.tac

#### Use

The demo application runs on port 8082.

On first run, the application asks for user initials. Press F4 to enter initials and change settings. Press F4 again to dismiss the settings pane. Press F1 for help. Press the space bar to dismiss any error boxes or information panes.

The interface is designed to be scanner-driven, so there is no visible text box for typing input. Hoewever, the appliction does accept typed input. Some example order numbers are AA00100, AA00300, and AA1230.

Christian Long

christianzlong@gmail.com

