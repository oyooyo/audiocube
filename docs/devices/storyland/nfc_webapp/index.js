const write_nfc_tag = async (...args) => {
	if (! ('NDEFReader' in window)) {
		throw (new Error(`This webbrowser does not support the Web NFC API. In practice, this means that you need an Android smartphone with Chrome v89 or later.`));
	}
	const ndef_reader = (new NDEFReader());
	await ndef_reader.write(...args);
}

const write_text_record_nfc_tag = (text) =>
	write_nfc_tag({records: [
		{data:text, recordType:'text', lang:'en'},
	]})

const fetch_predefined_nfc_tags = async () =>
	(await (await fetch('predefined_nfc_tags.json')).json())

const get_element = (id) =>
	document.getElementById(id)

const output_message = (message) => {
	get_element('message').value = message;
}

const setup = async () => {
	try {
		const nfc_tag_data_element = get_element('nfc_tag_data');
		const write_nfc_tag_element = get_element('write_nfc_tag_button');
		write_nfc_tag_element.onclick = async () => {
			try {
				output_message('Place NTAG213 NFC tag over NFC tag reader');
				const nfc_tag_data = nfc_tag_data_element.value.trim();
				await write_text_record_nfc_tag(nfc_tag_data);
				output_message('NFC Tag written successfully!');
			} catch(error) {
				output_message(`Error: ${error}`);
			}
		}
		const predefined_nfc_tags = await fetch_predefined_nfc_tags();
		const predefined_nfc_tags_element = get_element('predefined_nfc_tags');
		for (let predefined_nfc_tag of predefined_nfc_tags) {
			let [data, label] = predefined_nfc_tag;
			let option_element = document.createElement('option');
			option_element.setAttribute('value', data);
			option_element.appendChild(document.createTextNode(label));
			predefined_nfc_tags_element.appendChild(option_element);
		}
		predefined_nfc_tags_element.onchange = (event) => {
			nfc_tag_data_element.value = predefined_nfc_tags_element.value;
		}
	} catch(error) {
		output_message(`Error: ${error}`);
	}
}

setup();
