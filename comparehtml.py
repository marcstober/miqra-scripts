import pprint
import re
import html

approved = [
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיִּקְרָ֧א אֶת־שְׁמ֛וֹ נֹ֖חַ לֵאמֹ֑ר זֶ֞֠ה יְנַחֲמֵ֤נוּ "
        "מִֽמַּעֲשֵׂ֙נוּ֙ וּמֵעִצְּב֣וֹן יָדֵ֔ינוּ מִן־הָ֣אֲדָמָ֔ה אֲשֶׁ֥ר "
        "אֵֽרְרָ֖הּ יְהֹוָֽה׃",
        "line_number": 143,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיִּ֥יקֶץ נֹ֖חַ מִיֵּינ֑וֹ וַיֵּ֕דַע אֵ֛ת אֲשֶׁר־עָ֥שָׂה ל֖וֹ " "בְּנ֥וֹ הַקָּטָֽן׃",
        "line_number": 242,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיִּתֵּן֙ בְּיַד־עֲבָדָ֔יו עֵ֥דֶר עֵ֖דֶר לְבַדּ֑וֹ וַיֹּ֤אמֶר "
        "אֶל־עֲבָדָיו֙ עִבְר֣וּ לְפָנַ֔י וְרֶ֣וַח תָּשִׂ֔ימוּ בֵּ֥ין "
        "עֵ֖דֶר וּבֵ֥ין עֵֽדֶר׃",
        "line_number": 980,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וְנָק֥וּמָה וְנַעֲלֶ֖ה בֵּֽית־אֵ֑ל וְאֶֽעֱשֶׂה־שָּׁ֣ם מִזְבֵּ֗חַ "
        "לָאֵ֞ל הָעֹנֶ֤ה אֹתִי֙ בְּי֣וֹם צָֽרָתִ֔י וַֽיְהִי֙ עִמָּדִ֔י "
        "בַּדֶּ֖רֶךְ אֲשֶׁ֥ר הָלָֽכְתִּי׃",
        "line_number": 1053,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיֹּ֕אמֶר אָנֹכִ֛י אֲשַׁלַּ֥ח גְּדִֽי־עִזִּ֖ים מִן־הַצֹּ֑אן " "וַתֹּ֕אמֶר אִם־תִּתֵּ֥ן עֵרָב֖וֹן עַ֥ד שׇׁלְחֶֽךָ׃",
        "line_number": 1178,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ כְּהַיּ֣וֹם הַזֶּ֔ה וַיָּבֹ֥א הַבַּ֖יְתָה לַעֲשׂ֣וֹת "
        "מְלַאכְתּ֑וֹ וְאֵ֨ין אִ֜ישׁ מֵאַנְשֵׁ֥י הַבַּ֛יִת שָׁ֖ם "
        "בַּבָּֽיִת׃",
        "line_number": 1203,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ כִּרְאוֹתָ֔הּ כִּֽי־עָזַ֥ב בִּגְד֖וֹ בְּיָדָ֑הּ " "וַיָּ֖נׇס הַחֽוּצָה׃",
        "line_number": 1205,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ כִּ֣י עָלִ֔ינוּ אֶֽל־עַבְדְּךָ֖ אָבִ֑י וַנַּ֨גֶּד־ל֔וֹ " "אֵ֖ת דִּבְרֵ֥י אֲדֹנִֽי׃",
        "line_number": 1396,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיֹּ֤אמֶר אֲלֵהֶם֙ מֶ֣לֶךְ מִצְרַ֔יִם לָ֚מָּה מֹשֶׁ֣ה וְאַהֲרֹ֔ן "
        "תַּפְרִ֥יעוּ אֶת־הָעָ֖ם מִֽמַּעֲשָׂ֑יו לְכ֖וּ לְסִבְלֹתֵיכֶֽם׃",
        "line_number": 1696,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיֵּלְכ֥וּ וַֽיַּעֲשׂ֖וּ בְּנֵ֣י יִשְׂרָאֵ֑ל כַּאֲשֶׁ֨ר צִוָּ֧ה " "יְהֹוָ֛ה אֶת־מֹשֶׁ֥ה וְאַהֲרֹ֖ן כֵּ֥ן עָשֽׂוּ׃",
        "line_number": 1911,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיַּעֲשׂ֖וּ כׇּל־בְּנֵ֣י יִשְׂרָאֵ֑ל כַּאֲשֶׁ֨ר צִוָּ֧ה " "יְהֹוָ֛ה אֶת־מֹשֶׁ֥ה וְאֶֽת־אַהֲרֹ֖ן כֵּ֥ן עָשֽׂוּ׃",
        "line_number": 1933,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ מִֽמׇּחֳרָ֔ת וַיֵּ֥שֶׁב מֹשֶׁ֖ה לִשְׁפֹּ֣ט אֶת־הָעָ֑ם "
        "וַיַּעֲמֹ֤ד הָעָם֙ עַל־מֹשֶׁ֔ה מִן־הַבֹּ֖קֶר עַד־הָעָֽרֶב׃",
        "line_number": 2085,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ ק֣וֹל הַשֹּׁפָ֔ר הוֹלֵ֖ךְ וְחָזֵ֣ק מְאֹ֑ד מֹשֶׁ֣ה " "יְדַבֵּ֔ר וְהָאֱלֹהִ֖ים יַעֲנֶ֥נּוּ בְקֽוֹל׃",
        "line_number": 2119,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "לֹֽ֣א־תַעֲשֶֽׂ֨ה־לְךָ֥֣ פֶ֣֙סֶל֙ ׀ וְכׇל־תְּמוּנָ֔֡ה אֲשֶׁ֤֣ר "
        "בַּשָּׁמַ֣֙יִם֙ ׀ מִמַּ֔֡עַל וַֽאֲשֶׁ֥ר֩ בָּאָ֖֨רֶץ מִתָּ֑͏ַ֜חַת "
        "וַאֲשֶׁ֥ר בַּמַּ֖֣יִם ׀ מִתַּ֥֣חַת לָאָֽ֗רֶץ׃",
        "line_number": 2129,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "לֹֽא־תִשְׁתַּחֲוֶ֥֣ה לָהֶ֖ם֮ וְלֹ֣א תׇעׇבְדֵ֑ם֒ כִּ֣י אָֽנֹכִ֞י "
        "יְהֹוָ֤ה אֱלֹהֶ֙יךָ֙ אֵ֣ל קַנָּ֔א פֹּ֠קֵ֠ד עֲוֺ֨ן אָבֹ֧ת "
        "עַל־בָּנִ֛ים עַל־שִׁלֵּשִׁ֥ים וְעַל־רִבֵּעִ֖ים לְשֹׂנְאָֽ֑י׃",
        "line_number": 2130,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "לֹֽא־תִשְׁתַּחֲוֶ֤ה לֵאלֹֽהֵיהֶם֙ וְלֹ֣א תׇֽעׇבְדֵ֔ם וְלֹ֥א "
        "תַעֲשֶׂ֖ה כְּמַֽעֲשֵׂיהֶ֑ם כִּ֤י הָרֵס֙ תְּהָ֣רְסֵ֔ם וְשַׁבֵּ֥ר "
        "תְּשַׁבֵּ֖ר מַצֵּבֹתֵיהֶֽם׃",
        "line_number": 2242,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיִּשְׁלַ֗ח אֶֽת־נַעֲרֵי֙ בְּנֵ֣י יִשְׂרָאֵ֔ל וַֽיַּעֲל֖וּ " "עֹלֹ֑ת וַֽיִּזְבְּח֞וּ זְבָחִ֧ים שְׁלָמִ֛ים לַיהֹוָ֖ה פָּרִֽים׃",
        "line_number": 2257,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וְאֶל־אֲצִילֵי֙ בְּנֵ֣י יִשְׂרָאֵ֔ל לֹ֥א שָׁלַ֖ח יָד֑וֹ " "וַיֶּֽחֱזוּ֙ אֶת־הָ֣אֱלֹהִ֔ים וַיֹּאכְל֖וּ וַיִּשְׁתּֽוּ׃",
        "line_number": 2263,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ מִֽמׇּחֳרָ֔ת וַיֹּ֤אמֶר מֹשֶׁה֙ אֶל־הָעָ֔ם אַתֶּ֥ם "
        "חֲטָאתֶ֖ם חֲטָאָ֣ה גְדֹלָ֑ה וְעַתָּה֙ אֶֽעֱלֶ֣ה אֶל־יְהֹוָ֔ה "
        "אוּלַ֥י אֲכַפְּרָ֖ה בְּעַ֥ד חַטַּאתְכֶֽם׃",
        "line_number": 2551,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ בַּיּ֣וֹם הַשְּׁמִינִ֔י קָרָ֣א מֹשֶׁ֔ה לְאַהֲרֹ֖ן " "וּלְבָנָ֑יו וּלְזִקְנֵ֖י יִשְׂרָאֵֽל׃",
        "line_number": 3055,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַיִּקְרָ֣א מֹשֶׁ֗ה אֶל־מִֽישָׁאֵל֙ וְאֶ֣ל אֶלְצָפָ֔ן בְּנֵ֥י "
        "עֻזִּיאֵ֖ל דֹּ֣ד אַהֲרֹ֑ן וַיֹּ֣אמֶר אֲלֵהֶ֗ם קִ֞֠רְב֞֠וּ שְׂא֤וּ "
        "אֶת־אֲחֵיכֶם֙ מֵאֵ֣ת פְּנֵי־הַקֹּ֔דֶשׁ אֶל־מִח֖וּץ לַֽמַּחֲנֶֽה׃",
        "line_number": 3083,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ כְּכַלֹּת֔וֹ לְדַבֵּ֕ר אֵ֥ת כׇּל־הַדְּבָרִ֖ים הָאֵ֑לֶּה " "וַתִּבָּקַ֥ע הָאֲדָמָ֖ה אֲשֶׁ֥ר תַּחְתֵּיהֶֽם׃",
        "line_number": 4361,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "כֹּ֣ל ׀ תְּרוּמֹ֣ת הַקֳּדָשִׁ֗ים אֲשֶׁ֨ר יָרִ֥ימוּ "
        "בְנֵֽי־יִשְׂרָאֵל֮ לַֽיהֹוָה֒ נָתַ֣תִּֽי לְךָ֗ וּלְבָנֶ֧יךָ "
        "וְלִבְנֹתֶ֛יךָ אִתְּךָ֖ לְחׇק־עוֹלָ֑ם בְּרִית֩ מֶ֨לַח עוֹלָ֥ם "
        "הִוא֙ לִפְנֵ֣י יְהֹוָ֔ה לְךָ֖ וּֽלְזַרְעֲךָ֥ אִתָּֽךְ׃",
        "line_number": 4414,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ הַמַּלְק֔וֹחַ יֶ֣תֶר הַבָּ֔ז אֲשֶׁ֥ר בָּזְז֖וּ עַ֣ם "
        "הַצָּבָ֑א צֹ֗אן שֵׁשׁ־מֵא֥וֹת אֶ֛לֶף וְשִׁבְעִ֥ים אֶ֖לֶף "
        "וַחֲמֵ֥שֶׁת אֲלָפִֽים׃",
        "line_number": 4847,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וַֽיְהִי֙ בְּאַרְבָּעִ֣ים שָׁנָ֔ה בְּעַשְׁתֵּֽי־עָשָׂ֥ר חֹ֖דֶשׁ "
        "בְּאֶחָ֣ד לַחֹ֑דֶשׁ דִּבֶּ֤ר מֹשֶׁה֙ אֶל־בְּנֵ֣י יִשְׂרָאֵ֔ל "
        "כְּ֠כֹ֠ל אֲשֶׁ֨ר צִוָּ֧ה יְהֹוָ֛ה אֹת֖וֹ אֲלֵהֶֽם׃",
        "line_number": 5053,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "לֹא־תִשְׁתַּחֲוֶ֥֣ה לָהֶ֖ם֮ וְלֹ֣א תׇעׇבְדֵ֑ם֒ כִּ֣י אָנֹכִ֞י "
        "יְהֹוָ֤ה אֱלֹהֶ֙יךָ֙ אֵ֣ל קַנָּ֔א פֹּ֠קֵ֠ד עֲוֺ֨ן אָב֧וֹת "
        "עַל־בָּנִ֛ים וְעַל־שִׁלֵּשִׁ֥ים וְעַל־רִבֵּעִ֖ים לְשֹׂנְאָֽ֑י׃",
        "line_number": 5223,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וְי֨וֹם֙ הַשְּׁבִיעִ֔֜י שַׁבָּ֖֣ת ׀ לַיהֹוָ֣ה אֱלֹהֶ֑֗יךָ לֹ֣א "
        "תַעֲשֶׂ֣ה כׇל־מְלָאכָ֡ה אַתָּ֣ה וּבִנְךָֽ־וּבִתֶּ֣ךָ "
        "וְעַבְדְּךָֽ־וַ֠אֲמָתֶ֠ךָ וְשׁוֹרְךָ֨ וַחֲמֹֽרְךָ֜ "
        "וְכׇל־בְּהֶמְתֶּ֗ךָ וְגֵֽרְךָ֙ אֲשֶׁ֣ר בִּשְׁעָרֶ֔יךָ לְמַ֗עַן "
        "יָנ֛וּחַ עַבְדְּךָ֥ וַאֲמָתְךָ֖ כָּמֽ֑וֹךָ׃",
        "line_number": 5228,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "יִשָּׂ֣א יְהֹוָה֩ עָלֶ֨יךָ גּ֤וֹי מֵֽרָחֹק֙ מִקְצֵ֣ה הָאָ֔רֶץ "
        "כַּאֲשֶׁ֥ר יִדְאֶ֖ה הַנָּ֑שֶׁר גּ֕וֹי אֲשֶׁ֥ר לֹא־תִשְׁמַ֖ע "
        "לְשֹׁנֽוֹ׃",
        "line_number": 5841,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "הָרַכָּ֨ה בְךָ֜ וְהָעֲנֻגָּ֗ה אֲשֶׁ֨ר לֹֽא־נִסְּתָ֤ה "
        "כַף־רַגְלָהּ֙ הַצֵּ֣ג עַל־הָאָ֔רֶץ מֵהִתְעַנֵּ֖ג וּמֵרֹ֑ךְ "
        "תֵּרַ֤ע עֵינָהּ֙ בְּאִ֣ישׁ חֵיקָ֔הּ וּבִבְנָ֖הּ וּבְבִתָּֽהּ׃",
        "line_number": 5848,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וְנִשְׁאַרְתֶּם֙ בִּמְתֵ֣י מְעָ֔ט תַּ֚חַת אֲשֶׁ֣ר הֱיִיתֶ֔ם "
        "כְּכוֹכְבֵ֥י הַשָּׁמַ֖יִם לָרֹ֑ב כִּֽי־לֹ֣א שָׁמַ֔עְתָּ בְּק֖וֹל "
        "יְהֹוָ֥ה אֱלֹהֶֽיךָ׃",
        "line_number": 5854,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "פֶּן־יֵ֣שׁ בָּ֠כֶ֠ם אִ֣ישׁ אֽוֹ־אִשָּׁ֞ה א֧וֹ מִשְׁפָּחָ֣ה "
        "אוֹ־שֵׁ֗בֶט אֲשֶׁר֩ לְבָב֨וֹ פֹנֶ֤ה הַיּוֹם֙ מֵעִם֙ יְהֹוָ֣ה "
        "אֱלֹהֵ֔ינוּ לָלֶ֣כֶת לַעֲבֹ֔ד אֶת־אֱלֹהֵ֖י הַגּוֹיִ֣ם הָהֵ֑ם "
        "פֶּן־יֵ֣שׁ בָּכֶ֗ם שֹׁ֛רֶשׁ פֹּרֶ֥ה רֹ֖אשׁ וְלַעֲנָֽה׃",
        "line_number": 5879,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "וְעַתָּ֗ה כִּתְב֤וּ לָכֶם֙ אֶת־הַשִּׁירָ֣ה הַזֹּ֔את וְלַמְּדָ֥הּ "
        "אֶת־בְּנֵֽי־יִשְׂרָאֵ֖ל שִׂימָ֣הּ בְּפִיהֶ֑ם לְמַ֨עַן "
        "תִּֽהְיֶה־לִּ֜י הַשִּׁירָ֥ה הַזֹּ֛את לְעֵ֖ד בִּבְנֵ֥י "
        "יִשְׂרָאֵֽל׃",
        "line_number": 5931,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "הֵ֚ם קִנְא֣וּנִי בְלֹא־אֵ֔ל כִּעֲס֖וּנִי בְּהַבְלֵיהֶ֑ם וַֽאֲנִי֙ "
        "אַקְנִיאֵ֣ם בְּלֹא־עָ֔ם בְּג֥וֹי נָבָ֖ל אַכְעִיסֵֽם׃",
        "line_number": 5964,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "אֵיכָ֞ה יִרְדֹּ֤ף אֶחָד֙ אֶ֔לֶף וּשְׁנַ֖יִם יָנִ֣יסוּ רְבָבָ֑ה "
        "אִם־לֹא֙ כִּֽי־צוּרָ֣ם מְכָרָ֔ם וַֽיהֹוָ֖ה הִסְגִּירָֽם׃",
        "line_number": 5973,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "יוֹר֤וּ מִשְׁפָּטֶ֙יךָ֙ לְיַֽעֲקֹ֔ב וְתוֹרָתְךָ֖ לְיִשְׂרָאֵ֑ל " "יָשִׂ֤ימוּ קְטוֹרָה֙ בְּאַפֶּ֔ךָ וְכָלִ֖יל עַֽל־מִזְבְּחֶֽךָ׃",
        "line_number": 6006,
    },
    {
        "diff_type": "NOT OK but less than 2 characters added",
        "line_1": "אַשְׁרֶ֨יךָ יִשְׂרָאֵ֜ל מִ֣י כָמ֗וֹךָ עַ֚ם נוֹשַׁ֣ע בַּֽיהֹוָ֔ה "
        "מָגֵ֣ן עֶזְרֶ֔ךָ וַאֲשֶׁר־חֶ֖רֶב גַּאֲוָתֶ֑ךָ וְיִכָּחֲשׁ֤וּ "
        "אֹיְבֶ֙יךָ֙ לָ֔ךְ וְאַתָּ֖ה עַל־בָּמוֹתֵ֥ימוֹ תִדְרֹֽךְ׃",
        "line_number": 6025,
    },
    {
        "diff_type": "NOT OK, template removed BUT still NOT ok",
        "line_1": "וַיְהִ֗י בִּשְׁכֹּ֤ן יִשְׂרָאֵל֙ בָּאָ֣רֶץ הַהִ֔וא וַיֵּ֣לֶךְ "
        "רְאוּבֵ֗֔ן וַיִּשְׁכַּ֕ב֙ אֶת־בִּלְהָ֖ה֙ פִּילֶ֣גֶשׁ אָבִ֑֔יו "
        "וַיִּשְׁמַ֖ע יִשְׂרָאֵ֑͏ֽל׃ וַיִּֽהְי֥וּ בְנֵֽי־יַעֲקֹ֖ב שְׁנֵ֥ים "
        "עָשָֽׂר׃",
        "line_number": 1072,
    },
]
approved_indexed = {}
for approved_line in approved:
    approved_indexed[approved_line["line_number"]] = approved_line


file_path_0 = R"..\miqra-data\MAM-Torah-BASE.html"  # Replace with the actual file path
file_path_1 = (
    R"..\miqra-data\miqra-json-html\MAM-Torah.html"  # Replace with the actual file path
)

# Open the file in read mode
with open(file_path_0, "r", encoding="utf-8") as file:
    lines_0 = file.readlines()  # Read all lines from the file and store them in a list

# Open the file in read mode
with open(file_path_1, "r", encoding="utf-8") as file:
    lines_1 = file.readlines()  # Read all lines from the file and store them in a list


def split_verse_number(line):
    match = re.search(r"<h3>(\w+)</h3>(.*)", line)
    verse_number = match.group(1)
    text = match.group(2)
    return verse_number, text


def find_first_different_character(text_0, text_1):
    result = {}
    # find first different character
    for pos, chars in enumerate(zip(text_0, text_1)):
        char0, char1 = chars
        if char0 != char1:
            result["pos"] = pos
            result["char0"] = char0
            result["char1"] = char1
            result["hex0"] = hex(ord(char0))  # derived
            result["hex1"] = hex(ord(char1))  # derived
            return result


count_lines = 0
diffs = []
# Compare the two files
for line_0, line_1 in zip(lines_0, lines_1):
    count_lines += 1

    if line_1.startswith("<h1>"):
        current_book = re.sub(r"<.*?>", "", line_1)
    elif line_1.startswith("<h2>"):
        current_chapter = re.sub(r"<.*?>", "", line_1)

    if line_0 != line_1:
        _, text0 = split_verse_number(line_0)
        verse_number, text1 = split_verse_number(line_1)

        diffs.append(
            {
                "line_number": count_lines,
                "current_book": current_book,
                "current_chapter": current_chapter,
                "verse_number": verse_number,
                "line_0": text0,
                "line_1": text1,
                "line_0_len": len(text0),  # derived
                "line_1_len": len(text1),  # derived
                "diff_type": "NOT OK",
            }
        )


for diff in diffs:

    result = find_first_different_character(diff["line_0"], diff["line_1"])

    diff.update(result)

    # see if the diff is OK
    # if it's just removed meteg AND that's the only different, it's OK
    meteg_count_0 = diff["line_0"].count("\u05bd")  # HEBREW POINT METEG
    meteg_count_1 = diff["line_1"].count("\u05bd")  # HEBREW POINT METEG
    line_0_no_meteg = diff["line_0"].replace("\u05bd", "")
    line_1_no_meteg = diff["line_1"].replace("\u05bd", "")

    ok = False

    if line_0_no_meteg == line_1_no_meteg:
        if meteg_count_0 > meteg_count_1:
            diff["diff_type"] = "OK, meteg removed"
            ok = True

    # only difference is that original has this template showing that shouldn't have been anyway
    # may be replace in new source with combining grapheme joiner
    if not ok:
        line_0 = diff["line_0"]
        line_1 = diff["line_1"]
        if "מ:טעם ומתג באות אחת" in line_0:
            if "\u034f\u05bd" in line_1:  # combining grapheme joiner, meteg
                line_0_stripped = line_0.replace(
                    '<span style="color: red">TEMPLATE(</span><span style="color: #99f">מ:טעם ומתג באות אחת</span><span style="color: red">)</span>',
                    "",
                )
                line_1_stripped = line_1.replace(
                    "\u034f\u05bd", ""
                )  # combining grapheme joiner, meteg (how the same thing is encode in new source)
                diff["line_0_stripped"] = line_0_stripped  # debugging
                if line_0_stripped == line_1_stripped:  # combining grapheme joiner
                    diff["diff_type"] = "OK, template removed, CJG+meteg added"
                    ok = True
                else:
                    diff["diff_type"] = "NOT OK, template removed BUT still NOT ok"
                    rec = find_first_different_character(
                        line_0_stripped, line_1_stripped
                    )
                    diff["recompare"] = {
                        "line_0_len": len(line_0_stripped),
                        "line_1_len": len(line_1_stripped),
                    }
                    diff["recompare"].update(rec)

    if not ok:
        added_len = diff["line_1_len"] - diff["line_0_len"]
        if added_len >= 0 and added_len <= 2:
            diff["diff_type"] = "NOT OK but less than 2 characters added"

    if not ok:
        line_0 = diff["line_0"]
        line_1 = diff["line_1"]
        if "&gt;" in line_0 and "&lt;" in line_0:
            line_0_stripped = re.sub(r"&lt;.*?&gt;", "", line_0)
            # line_0_stripped = re.sub(r"\<.*?\>", "", line_0)
            diff["line_0_stripped"] = line_0_stripped  # debugging
            if line_0_stripped == line_1:
                diff["diff_type"] = (
                    "OK, removed custom tag that was badly handled in previous parshio version"
                )
                ok = True
            else:
                rec = find_first_different_character(line_0_stripped, line_1_stripped)
                diff["recompare"] = {
                    "line_0_len": len(line_0_stripped),
                    "line_1_len": len(line_1_stripped),
                }
                diff["recompare"].update(rec)

    if not ok:
        approved_line = approved_indexed.get(diff["line_number"])
        if approved_line:
            if diff["line_1"] == approved_line["line_1"]:
                diff["diff_type"] = "OK, approved"
                ok = True

# organize by diff type
diffs_by_type = {}
for diff in diffs:
    diff_type = diff.get("diff_type", "other")
    if diff_type not in diffs_by_type:
        diffs_by_type[diff_type] = []
    diffs_by_type[diff_type].append(diff)

# Output to HTML file
# Sort the dictionary by keys
# diffs_by_type = sorted(diffs_by_type.items())

with open("comparehtml.html", "w", encoding="utf-8") as file:
    file.write("<html>\n")
    file.write("<head>\n")
    file.write("<title>Comparison Results</title>\n")
    file.write("<link rel='stylesheet' href='comparehtml.css'>\n")
    file.write("</head>\n")
    file.write("<body>\n")
    file.write("<h1>Comparison Results</h1>\n")
    file.write("<p>0 has {} lines</p>\n".format(len(lines_0)))
    file.write("<p>1 has {} lines</p>\n".format(len(lines_1)))
    file.write("<p>Total differences: {}</p>\n".format(len(diffs)))
    for diff_type in sorted(diffs_by_type):
        file.write("<details>\n")
        file.write(f"<summary>\n")
        file.write(f"<h2>{diff_type}</h2>\n")
        file.write(f"<p>{len(diffs_by_type[diff_type])} differences</p>\n")
        file.write("</summary>\n")
        for diff in diffs_by_type[diff_type]:
            file.write("<p class='diff-text'>\n")
            file.write(html.escape(diff["line_0"]))
            file.write("</p>\n")
            file.write("<p class='diff-text'>\n")
            file.write(html.escape(diff["line_1"]))
            file.write("</p>\n")
            file.write("<pre>\n")
            pprint.pprint(diff, stream=file, width=100)
            file.write("</pre>\n")
        file.write("</details>\n")

    # once you have checked that the remaining differences are OK,
    # you can copy this output and paste above
    file.write("<textarea rows='20' cols='100'>\n")
    approved_out = []
    for diff_type in sorted(diffs_by_type):
        if diff_type.startswith("NOT OK"):
            for diff in diffs_by_type[diff_type]:
                approved_out.append(
                    {
                        "line_number": diff["line_number"],
                        "line_1": diff["line_1"],
                        "diff_type": diff["diff_type"],
                    }
                )
    file.write(pprint.pformat(approved_out))
    file.write("</textarea>\n")

    file.write("</body>\n")
    file.write("</html>\n")


print("Comparison results saved to comparehtml.html")
