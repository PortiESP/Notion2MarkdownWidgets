import {Title, Title2, Title3, Title4, Link, Paragraph, UList, Img, Callout, Code, SubPage, Quote, Url, Toggle, Block, Hr, Section} from "@/components/MarkupWidgets/Tags.js"



export default function Page(){ return (<>

	<Title>MyTitle</Title>

	<Title2>MyTitle2</Title2>

	<Title3>MyTitle3</Title3>

	<Paragraph>Template text</Paragraph>

	<Hr />

	<Paragraph>TestINI</Paragraph>

	<Code >const data = "test"</Code>

	<Image alt={"Alt text"} src={"https://cdn.sstatic.net/Img/home/illo-public.svg?v=14bd5a506009"} />

</>)}