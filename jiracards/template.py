
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

        #page {
            width: 100%;
            margin: 0; padding: 0;
            background: none;
        }

        #content {
            width: 620px;
            margin: auto;
        }

        .content-column-1 {
            width: 300;
            float: left;
            margin-right: 10px;
        }

        .content-column-2 {
            width: 300;
            float: right;
        }

        .ticket-item {
            position: relative;
            background-color: #FFF;
            border: 4px solid rgba(255, 0, 0, 1.0);
            border-radius: 5px 5px 5px 5px;
            margin-bottom: 15px;
            min-height: 170px;
            page-break-before : right;
        }

        .header {
            position: relative;
            background-color: #FF0000;
            height: 30px;
        }

        .title {
            padding-left: 10px;
            padding-top: 1px;
            color: #FFF;
            font-size: 22px;
            font-weight: bold;
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
    <div id="page">
        <div id="content">
            {% for column in tickets | slice(2) %}
                <div class="content-column-{{ loop.index }}">
                    {% for ticket in column %}
                        <div class="ticket-item" style="border-color: {{ ticket.cardcolor }}">
                            <div class="header" style="background-color: {{ ticket.cardcolor }}">
                                <div class="title">{{ ticket.key }}</div>
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
    </div>
</body>
</html>
"""
