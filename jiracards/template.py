
DEFAULT_TEMPLATE="""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title>Jira Cards</title>

    <style type="text/css">
        body {
            font-family: Georgia, serif;
            background: none;
            color: black;
        }

        #page-container {
            display: block;
            width: 100%;
            margin: 0; padding: 0;
            background: none;
        }

        .page:first-child {
            clear: both;
        }

        .page:not(:first-child) {
            page-break-before: always;
            clear: both;
        }

        .ticket-item {
            position: relative;
            float: left;
            height: 170px;
            width: 300px;
            margin: auto;
            background-color: #FFF;
            border: 4px solid rgba(255, 0, 0, 1.0);
            border-radius: 5px 5px 5px 5px;
            margin-left: 15px;
            margin-bottom: 15px;
            page-break-before : right;
        }

        .header {
            display: block;
            position: relative;
            background-color: #FF0000;
            height: 30px;
        }

        .title {
            float: left;
            width: 180px;
            padding-left: 10px;
            padding-top: 1px;
            color: #FFF;
            font-size: 22px;
            font-weight: bold;
        }

        .ticket-type {
            float: right;
            position: relative;
            margin-top: 4px;
            margin-right: 10px;
            font-size: 10px;
            color: #FFF;
        }

        .summary {
            float: left;
            width: 160px;
            padding: 15px;
        }

        .summary-text {
            font-size: 16px;
            font-weight: bold;
            color: #000;
        }

        .dod-container {
            position: relative;
            display: inline-block;
            float: right;
            width: 100px;
            min-height: 140px;
            background-color: #FFF;
        }

        .dod-header {
            font-size: 16px;
            font-weight: bold;
            color: #FFF;
            margin-left: 35px;
        }

        .dod-item {
            display: inline-block;
            width: 80px;
            height: 20px;
        }

        .dod-box {
            display: inline-block;
            margin-left: 5px;
            height: 15px;
            width: 15px;
            background-color: #FFF;
        }

        .dod-text {
            display: inline-block;
            position: relative;
            font-size: 11px;
            font-weight: bold;
            color: #FFF;
            margin-bottom: 4px;
        }
        </style>
</head>
<body>
    <div id="page-container">
        {% for row in tickets | batch(10) %}
            <div class="page">
            {% for ticket in row %}
                <div class="ticket-item" style="border-color: {{ ticket.cardcolor }}">
                    <div class="header" style="background-color: {{ ticket.cardcolor }}">
                        <div class="title">{{ ticket.key }}</div>
                        <div class="ticket-type">{{ ticket.typeName }}</div>
                    </div>
                    <div class="summary">
                        <div class="summary-text">
                            {{ ticket.summary }}
                        </div>
                    </div>
                    <div class="dod-container" style="border-left: 2px solid {{ ticket.cardcolor }}">
                        <div class="dod-header" style="color: {{ ticket.cardcolor }}">DoD</div>
                        <div class="dod-item">
                            <div class="dod-box" style="border: 1px solid {{ ticket.cardcolor }}"></div>
                            <div class="dod-text" style="color: {{ ticket.cardcolor }}">Doku</div>
                        </div>
                        <div class="dod-item">
                            <div class="dod-box" style="border: 1px solid {{ ticket.cardcolor }}"></div>
                            <div class="dod-text" style="color: {{ ticket.cardcolor }}">Tests</div>
                        </div>
                        <div class="dod-item">
                            <div class="dod-box" style="border: 1px solid {{ ticket.cardcolor }}"></div>
                            <div class="dod-text" style="color: {{ ticket.cardcolor }}">Build OK</div>
                        </div>
                        <div class="dod-item">
                            <div class="dod-box" style="border: 1px solid {{ ticket.cardcolor }}"></div>
                            <div class="dod-text" style="color: {{ ticket.cardcolor }}">Merged</div>
                        </div>
                        <div class="dod-item">
                            <div class="dod-box" style="border: 1px solid {{ ticket.cardcolor }}"></div>
                            <div class="dod-text" style="color: {{ ticket.cardcolor }}">Released</div>
                        </div>
                    </div>
                </div>
            {% endfor %}
            </div>
        {% endfor %}
    </div>
</body>
</html>
"""
